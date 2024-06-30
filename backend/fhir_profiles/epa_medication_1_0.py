from fhir.resources.R4B.medication import Medication
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.extension import Extension
from fhir.resources.R4B.ratio import Ratio
from fhir.resources.R4B.quantity import Quantity
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.reference import Reference
from fhir.resources.R4B.bundle import Bundle, BundleEntry
import uuid
import json


class EpaMedication1_0:
    def to_dict(self, obj):
        """
        Recursively convert a MedicinalProduct object (or any custom object) to a dictionary.
        """
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
            return self.build_single_medical_produkt(data)
        else:
            return self.build_multiple_medical_produkt(data)

    def build_extension(self, url, system=None, code=None, display=None, value=None, version=None):
        if system and code and display:
            return Extension(
                url=url,
                valueCoding=Coding(system=system, code=code,
                                   display=display, version=version)
            )
        elif isinstance(value, bool):
            return Extension(url=url, valueBoolean=value)
        elif isinstance(value, str):
            return Extension(url=url, valueString=value)
        elif isinstance(value, int):
            return Extension(url=url, valueInteger=value)
        return None

    def build_ingredient(self, substance):
        return {
            "itemCodeableConcept": CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc",
                           code="[Insert ATC]",
                           display="[Insert ATC]"),
                    Coding(system="http://fhir.de/CodeSystem/ask",
                           code=substance.substance_id,
                           display=substance.name),
                    Coding(system="http://snomed.info/sct",
                           code="[Insert Snomed Code]",
                           display="[Insert Snomed Name]",
                           version="http://snomed.info/sct/900000000000207008/version/20240201")
                ]
            ),

            "strength": Ratio(
                numerator=Quantity(
                    value=float(substance.strength.split()[0]),
                    unit=substance.strength.split()[1],
                    system="http://unitsofmeasure.org",
                    code=substance.strength.split()[1]
                ),
                denominator=Quantity(value=1,
                                     unit="[Insert Denominator Unit]",
                                     system="http://unitsofmeasure.org",
                                     code="[Insert Denominator Code]")
            )
        }

    def build_medication(self, med_id, profile, type_code, type_display, identifier_value, code_system, code_value, code_display, lot_number, ingredients):
        return Medication(
            id=med_id,
            meta=Meta(profile=[profile]),
            extension=[
                ext for ext in [
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        system="http://snomed.info/sct",
                        code=type_code,
                        display=type_display,
                        version="http://snomed.info/sct/900000000000207008/version/20240201"
                    )
                ] if ext is not None
            ],
            identifier=[
                Identifier(
                    system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                    value=identifier_value
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(system=code_system, code=code_value,
                           display=code_display)
                ]
            ),
            ingredient=ingredients,
            batch={"lotNumber": lot_number}
        )

    def build_multiple_medical_produkt(self, data):
        medications = []
        for product in data.pharmaceutical_products:
            ingredients = [self.build_ingredient(
                substance) for substance in product.substances]
            medication = self.build_medication(
                med_id=product.key,
                profile="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-pharmaceutical-product",
                type_code="373873005",
                type_display="Pharmaceutical / biologic product (product)",
                identifier_value=str(uuid.uuid4()),
                code_system="http://fhir.de/CodeSystem/abdata/Komponentennummer",
                code_value=product.key,
                code_display=product.name,
                lot_number="[Insert Lot Number]",
                ingredients=ingredients
            )
            medications.append(medication)

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(profile=[
                      "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication"]),
            extension=[
                ext for ext in [
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        system="http://snomed.info/sct",
                        code="781405001",
                        display="Medicinal product package (product)",
                        version="http://snomed.info/sct/900000000000207008/version/20240201"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/drug-category-extension",
                        system="https://gematik.de/fhir/dev-epa-medication/CodeSystem/epa-drug-category-cs",
                        code="00"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-id-vaccine-extension",
                        value=False
                    ),
                    self.build_extension(
                        url="http://fhir.de/StructureDefinition/normgroesse",
                        value=getattr(data, 'normgroesse',
                                      '[Insert Normgroesse]')
                    )
                ] if ext is not None
            ],
            code=CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/ifa/pzn",
                           code=str(data.pzn),
                           display=getattr(data, 'artikelname', '[Insert Artikelname]')),
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc",
                           code="[Insert ATC]",
                           display="[Insert ATC]")
                ]
            ),
            form=CodeableConcept(
                coding=[
                    Coding(system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                           code=getattr(data, 'kbv_dar', '[Insert KBV Form Code]'))
                ]
            ),
            contained=medications,
            ingredient=[
                {"itemReference": Reference(reference=f"#{product.key}")} for product in data.pharmaceutical_products
            ]
        )

        return medication

    def build_single_medical_produkt(self, data):
        ingredients = [self.build_ingredient(
            substance) for substance in data.pharmaceutical_products[0].substances]

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(profile=[
                      "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication"]),
            extension=[
                ext for ext in [
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        system="http://snomed.info/sct",
                        code="781405001",
                        display="Medicinal product package (product)",
                        version="http://snomed.info/sct/900000000000207008/version/20240201"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/drug-category-extension",
                        system="https://gematik.de/fhir/dev-epa-medication/CodeSystem/epa-drug-category-cs",
                        code="00"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-id-vaccine-extension",
                        value=False
                    ),
                    self.build_extension(
                        url="http://fhir.de/StructureDefinition/normgroesse",
                        value=getattr(data, 'normgroesse',
                                      '[Insert Normgroesse]')
                    )
                ] if ext is not None
            ],
            identifier=[
                Identifier(
                    system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                    value=str(uuid.uuid4())
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/ifa/pzn", code=str(data.pzn),
                           display=getattr(data, 'artikelname', '[Insert Artikelname]')),
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc",
                                  code="[Insert ATC]",
                                  display="[Insert ATC]")
                ]
            ),
            form=CodeableConcept(
                coding=[
                    Coding(system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                           code=getattr(data, 'kbv_dar', '[Insert KBV Form Code]'))
                ]
            ),
            amount=Ratio(
                numerator=Quantity(
                    value=0,
                    unit="[Insert Total Quantity Formulation Unit]",
                    extension=[
                        ext for ext in [
                            self.build_extension(
                                url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-total-quantity-formulation-extension",
                                value="[Insert Total Quantity Formulation]"
                            )
                        ] if ext is not None
                    ]
                ),
                denominator=Quantity(value=1,
                                     unit="[Insert Denominator Unit]",
                                     system="http://unitsofmeasure.org",
                                     code="[Insert Denominator Code]")
            ),
            ingredient=ingredients
        )
        return medication

    def build_rezeptur_medical_produkt(self, data):
        ingredients = []
        contained_medications = []

        # Assuming that there's only one pharmaceutical product for a single medication
        for product in data.pharmaceutical_products:
            for substance in product.substances:
                contained_medication = Medication(
                    id=substance.key,
                    meta=Meta(profile=[
                              "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-pzn-ingredient"]),
                    extension=[
                        self.build_extension(
                            url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                            system="http://snomed.info/sct",
                            code="781405001",
                            display="Medicinal product package (product)",
                            version="http://snomed.info/sct/900000000000207008/version/20240201"
                        )
                    ],
                    code=CodeableConcept(
                        coding=[
                            Coding(system="http://fhir.de/CodeSystem/ifa/pzn",
                                   code=substance.key, display="[Insert Artikelname]"),
                            Coding(system="http://fhir.de/CodeSystem/bfarm/atc",
                                          code="[Insert ATC]",
                                          display="[Insert ATC]")
                        ]
                    ),
                    # Use actual lot number if available
                    batch={"lotNumber": substance.key}
                )
                contained_medications.append(contained_medication)

                ingredient = {
                    "itemReference": Reference(reference=f"#{substance.key}"),
                    "isActive": True,
                    "strength": Ratio(
                        numerator=Quantity(
                            value=float(substance.strength.split()[0]),
                            unit=substance.strength.split()[1],
                            system="http://unitsofmeasure.org",
                            code=substance.strength.split()[1]
                        ),
                        denominator=Quantity(value=1,
                                             unit="[Insert Denominator Unit]",
                                             system="http://unitsofmeasure.org",
                                             code="[Insert Denominator Code]")
                    )
                }
                ingredients.append(ingredient)

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(profile=[
                      "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication"]),
            extension=[
                ext for ext in [
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        system="http://snomed.info/sct",
                        code="781405001",
                        display="Medicinal product package (product)",
                        version="http://snomed.info/sct/900000000000207008/version/20240201"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/drug-category-extension",
                        system="https://gematik.de/fhir/dev-epa-medication/CodeSystem/epa-drug-category-cs",
                        code="00"
                    ),
                    self.build_extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-id-vaccine-extension",
                        value=False
                    ),
                    self.build_extension(
                        url="http://fhir.de/StructureDefinition/normgroesse",
                        value=getattr(data, 'normgroesse',
                                      '[Insert Normgroesse]')
                    )
                ] if ext is not None
            ],
            code=CodeableConcept(
                coding=[
                    Coding(system="http://fhir.de/CodeSystem/ifa/pzn", code=str(data.pzn),
                           display=getattr(data, 'name', '[Insert Artikelname]')),
                    Coding(system="http://fhir.de/CodeSystem/bfarm/atc",
                                  code="[Insert ATC]",
                                  display="[Insert ATC]")
                ]
            ),
            form=CodeableConcept(
                coding=[
                    Coding(system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                           code=getattr(data, 'kbv_dar', '[Insert KBV Form Code]'))
                ]
            ),
            amount=Ratio(
                numerator=Quantity(
                    value=0,
                    unit="[Insert Total Quantity Formulation Unit]",
                    extension=[
                        ext for ext in [
                            self.build_extension(
                                url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-total-quantity-formulation-extension",
                                value="[Insert Total Quantity Formulation]"
                            )
                        ] if ext is not None
                    ]
                ),
                denominator=Quantity(value=1,
                                     unit="[Insert Denominator Unit]",
                                     system="http://unitsofmeasure.org",
                                     code="[Insert Denominator Code]")
            ),
            ingredient=ingredients,
            contained=contained_medications
        )
        return medication
