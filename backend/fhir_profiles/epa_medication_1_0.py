from fhir.resources.R4B.medication import Medication
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.ratio import Ratio
from fhir.resources.R4B.quantity import Quantity
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.reference import Reference
import uuid
import json


class EpaMedication1_0:
    def to_dict(self, obj):
        if isinstance(obj, dict):
            return {k: self.to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, "_ast"):
            return self.to_dict(obj._ast())
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.to_dict(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return {key: self.to_dict(value) for key, value in obj.__dict__.items() if not callable(value) and not key.startswith('_')}
        else:
            return obj

    def create(self, data):
        data_dict = self.to_dict(data)
        print(json.dumps(data_dict, indent=4))

        if getattr(data, 'multiple_ppt', None) == 0:
            return self.build_medical_product(data)
        else:
            return self.build_kombiepackung(data)

    def build_extension(self, url, system=None, code=None, display=None, value=None, version=None):
        if system and code and display:
            return Extension(
                url=url,
                valueCoding=Coding(system=system, code=code, display=display, version=version)
            )
        if isinstance(value, bool):
            return Extension(url=url, valueBoolean=value)
        if isinstance(value, str):
            return Extension(url=url, valueString=value)
        if isinstance(value, int):
            return Extension(url=url, valueInteger=value)
        if url == "http://fhir.de/StructureDefinition/normgroesse" and isinstance(value, str):
            return Extension(url=url, valueCode=value)
        return None

    def build_ingredient(self, substance):
        strength_value, strength_unit = substance.strength.split()
        denominator_unit = "[Insert Denominator Unit]" if substance.denominator_unit else "1"
        denominator_code = "[Insert Denominator Code]" if substance.denominator_code else "#1"
        coding_list = [
            Coding(system="http://fhir.de/CodeSystem/bfarm/atc", code="[Insert ATC]" if substance.atc else None, display="[Insert ATC]" if substance.atc else None),
            Coding(system="http://fhir.de/CodeSystem/ask", code=substance.substance_id, display=substance.name)
        ]
        if substance.snomed_code:
            coding_list.append(Coding(system="http://snomed.info/sct", code=substance.snomed_code, display=substance.snomed_name, version="http://snomed.info/sct/900000000000207008/version/20240201"))

        return {
            "itemCodeableConcept": CodeableConcept(coding=[c for c in coding_list if c.code]),
            "isActive": True,
            "strength": Ratio(
                numerator=Quantity(value=float(strength_value), unit=strength_unit, system="http://unitsofmeasure.org", code=strength_unit),
                denominator=Quantity(value=1, unit=denominator_unit, system="http://unitsofmeasure.org", code=denominator_code)
            )
        }

    def build_medication(self, med_id, profile, type_code, type_display, identifier_value, code_system, code_value, code_display, lot_number, ingredients):
        extensions = [
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-type-extension",
                system="http://snomed.info/sct",
                code=type_code,
                display=type_display,
                version="http://snomed.info/sct/900000000000207008/version/20240201"
            )
        ]
        extensions = [ext for ext in extensions if ext is not None]

        return Medication(
            id=med_id,
            meta=Meta(profile=[profile]),
            extension=extensions,
            identifier=[Identifier(system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier", value=identifier_value)],
            code=CodeableConcept(coding=[Coding(system=code_system, code=code_value, display=code_display)]),
            ingredient=ingredients,
            batch={"lotNumber": lot_number}
        )

    def build_kombiepackung(self, data):
        medications = [
            self.build_medication(
                med_id=product.key,
                profile="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-pharmaceutical-product",
                type_code="373873005",
                type_display="Pharmaceutical / biologic product (product)",
                identifier_value=str(uuid.uuid4()),
                code_system="http://fhir.de/CodeSystem/abdata/Komponentennummer",
                code_value=product.key,
                code_display=product.name,
                lot_number="[Insert Lot Number]",
                ingredients=[self.build_ingredient(substance) for substance in product.substances]
            )
            for product in data.pharmaceutical_products
        ]

        common_extensions = [
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-type-extension",
                system="http://snomed.info/sct",
                code="781405001",
                display="Medicinal product package (product)",
                version="http://snomed.info/sct/900000000000207008/version/20240201"
            ),
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/drug-category-extension",
                system="https://gematik.de/fhir/epa-medication/CodeSystem/epa-drug-category-cs",
                code="00"
            ),
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/medication-id-vaccine-extension",
                value=False
            ),
            self.build_extension(
                url="http://fhir.de/StructureDefinition/normgroesse",
                value=getattr(data, 'normgroesse', '[Insert Normgroesse]')
            )
        ]
        common_extensions = [ext for ext in common_extensions if ext is not None]

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(profile=["https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication"]),
            extension=common_extensions,
            code=CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/ifa/pzn", code=str(data.pzn), display=getattr(data, 'artikelname', '[Insert Artikelname]')),
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc", code="[Insert ATC]" if data.atc else None, display="[Insert ATC]" if data.atc else None)
                ]
            ),
            form=CodeableConcept(coding=[Coding(system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM", code=getattr(data, 'kbv_dar', 'KPG') if data.multiple_ppt > 0 else '[Insert KBV Form Code]')]),
            contained=medications,
            ingredient=[{"itemReference": Reference(reference=f"#{product.key}")} for product in data.pharmaceutical_products]
        )

        return medication

    def build_medical_product(self, data):
        ingredients = [self.build_ingredient(substance) for substance in data.pharmaceutical_products[0].substances]

        common_extensions = [
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-type-extension",
                system="http://snomed.info/sct",
                code="781405001",
                display="Medicinal product package (product)",
                version="http://snomed.info/sct/900000000000207008/version/20240201"
            ),
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/drug-category-extension",
                system="https://gematik.de/fhir/epa-medication/CodeSystem/epa-drug-category-cs",
                code="00"
            ),
            self.build_extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/medication-id-vaccine-extension",
                value=False
            ),
            self.build_extension(
                url="http://fhir.de/StructureDefinition/normgroesse",
                value=getattr(data, 'normgroesse', '[Insert Normgroesse]')
            )
        ]
        common_extensions = [ext for ext in common_extensions if ext is not None]

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(profile=["https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication"]),
            extension=common_extensions,
            identifier=[Identifier(system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier", value=str(uuid.uuid4()))],
            code=CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/ifa/pzn", code=str(data.pzn), display=getattr(data, 'artikelname', '[Insert Artikelname]')),
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc", code="[Insert ATC]" if data.atc else None, display="[Insert ATC]" if data.atc else None)
                ]
            ),
            form=CodeableConcept(coding=[Coding(system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM", code=getattr(data, 'kbv_dar', '[Insert KBV Form Code]'))]),
            amount=Ratio(
                numerator=Quantity(
                    value=0,
                    unit="[Insert Total Quantity Formulation Unit]",
                    extension=[
                        self.build_extension(
                            url="https://gematik.de/fhir/epa-medication/StructureDefinition/medication-total-quantity-formulation-extension",
                            value="[Insert Total Quantity Formulation]"
                        )
                    ]
                ),
                denominator=Quantity(value=1, unit="[Insert Denominator Unit]" if data.denominator_unit else "1", system="http://unitsofmeasure.org", code="[Insert Denominator Code]" if data.denominator_code else "#1")
            ),
            ingredient=ingredients
        )
        return medication