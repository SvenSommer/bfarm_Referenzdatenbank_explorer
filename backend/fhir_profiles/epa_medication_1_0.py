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
            data = dict([(key, self.to_dict(value)) for key, value in obj.__dict__.items()
                         if not callable(value) and not key.startswith('_')])
            return data
        else:
            return obj

    def create(self, data):
        data_dict = self.to_dict(data)
        print(json.dumps(data_dict, indent=4))

        if getattr(data, 'multiple_ppt', None) == 0:
            return self.build_single_medical_produkt(data)
        else:
            return self.build_multiple_medical_produkt(data)

    def build_multiple_medical_produkt(self, data):
        contained_medications = [
            Medication(
                id="Augentropfen",
                meta=Meta(
                    profile=[
                        "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-pharmaceutical-product"
                    ]
                ),
                extension=[
                    Extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        valueCoding=Coding(
                            system="http://snomed.info/sct",
                            version="http://snomed.info/sct/900000000000207008/version/20240201",
                            code="373873005",
                            display="Pharmaceutical / biologic product (product)"
                        )
                    )
                ],
                identifier=[
                    Identifier(
                        system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                        value="59F8B8EF490A2A6D49C66D8C02574AB1E7C2EA97AEB925343F86D32616365984"
                    )
                ],
                code=CodeableConcept(
                    coding=[
                        Coding(
                            system="http://fhir.de/CodeSystem/abdata/Komponentennummer",
                            code="01746517-1",
                            display="Augentropfen"
                        )
                    ]
                ),
                ingredient=[
                    {
                        "itemCodeableConcept": CodeableConcept(
                            coding=[
                                Coding(
                                    system="http://fhir.de/CodeSystem/bfarm/atc",
                                    code="R01AC01",
                                    display="Natriumcromoglicat"
                                )
                            ]
                        ),
                        "strength": Ratio(
                            numerator=Quantity(
                                value=20,
                                unit="mg",
                                system="http://unitsofmeasure.org",
                                code="mg"
                            ),
                            denominator=Quantity(
                                value=1,
                                unit="ml",
                                system="http://unitsofmeasure.org",
                                code="ml"
                            )
                        )
                    }
                ],
                batch={
                    "lotNumber": "0132456"
                }
            ),
            Medication(
                id="NasenSpray",
                meta=Meta(
                    profile=[
                        "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-pharmaceutical-product"
                    ]
                ),
                extension=[
                    Extension(
                        url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                        valueCoding=Coding(
                            system="http://snomed.info/sct",
                            version="http://snomed.info/sct/900000000000207008/version/20240201",
                            code="373873005",
                            display="Pharmaceutical / biologic product (product)"
                        )
                    )
                ],
                identifier=[
                    Identifier(
                        system="https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                        value="FFE864A95C512A02207CDE2F38A0A21786FC5EC5E80491B2660C019CBC59ADA4"
                    )
                ],
                code=CodeableConcept(
                    coding=[
                        Coding(
                            system="http://fhir.de/CodeSystem/abdata/Komponentennummer",
                            code="01746517-2",
                            display="Nasenspray, Lösung"
                        )
                    ]
                ),
                ingredient=[
                    {
                        "itemCodeableConcept": CodeableConcept(
                            coding=[
                                Coding(
                                    system="http://fhir.de/CodeSystem/bfarm/atc",
                                    code="R01AC01",
                                    display="Natriumcromoglicat"
                                )
                            ]
                        ),
                        "strength": Ratio(
                            numerator=Quantity(
                                value=20,
                                unit="mg",
                                system="http://unitsofmeasure.org",
                                code="mg"
                            ),
                            denominator=Quantity(
                                value=1,
                                unit="ml",
                                system="http://unitsofmeasure.org",
                                code="ml"
                            )
                        )
                    }
                ],
                batch={
                    "lotNumber": "56498416854"
                }
            )
        ]

        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(
                profile=[
                    "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication"
                ]
            ),
            extension=[
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                    valueCoding=Coding(
                        system="http://snomed.info/sct",
                        version="http://snomed.info/sct/900000000000207008/version/20240201",
                        code="781405001",
                        display="Medicinal product package (product)"
                    )
                ),
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/drug-category-extension",
                    valueCoding=Coding(
                        system="https://gematik.de/fhir/dev-epa-medication/CodeSystem/epa-drug-category-cs",
                        code="00"
                    )
                ),
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-id-vaccine-extension",
                    valueBoolean=False
                ),
                Extension(
                    url="http://fhir.de/StructureDefinition/normgroesse",
                    valueCode=getattr(data, 'normgroesse',
                                      '[Insert Normgroesse]')
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://fhir.de/CodeSystem/ifa/pzn",
                        code=getattr(data, 'pzn', '[Insert PZN]')
                    )
                ],
                text=getattr(data, 'Artikelname', '[Insert Article Name]')
            ),
            form=CodeableConcept(
                coding=[
                    Coding(
                        system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                        code=getattr(data, 'form_code',
                                     '[Insert Form Code]')
                    )
                ]
            ),
            contained=contained_medications,
            ingredient=[
                {
                    "itemReference": Reference(
                        reference="#NasenSpray"
                    )
                },
                {
                    "itemReference": Reference(
                        reference="#Augentropfen"
                    )
                }
            ]
        )

        bundle = Bundle(
            type="searchset",
            entry=[BundleEntry(resource=medication)]
        )

        return bundle

    def build_single_medical_produkt(self, data):
        medication = Medication(
            id=str(uuid.uuid4()),
            meta=Meta(
                profile=[
                    "https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication"
                ]
            ),
            extension=[
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/epa-medication-type-extension",
                    valueCoding=Coding(
                        system="http://snomed.info/sct",
                        version="http://snomed.info/sct/900000000000207008/version/20240201",
                        code="781405001",
                        display="Medicinal product package (product)"
                    )
                ),
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/drug-category-extension",
                    valueCoding=Coding(
                        system="https://gematik.de/fhir/dev-epa-medication/CodeSystem/epa-drug-category-cs",
                        code="00"
                    )
                ),
                Extension(
                    url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-id-vaccine-extension",
                    valueBoolean=False
                ),
                Extension(
                    url="http://fhir.de/StructureDefinition/normgroesse",
                    valueCode=getattr(data, 'normgroesse',
                                      '[Insert Normgroesse]')
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://fhir.de/CodeSystem/ifa/pzn",
                        code=getattr(data, 'pzn', '[Insert PZN]')
                    )
                ],
                text=getattr(data, 'Artikelname', '[Insert Article Name]')
            ),
            form=CodeableConcept(
                coding=[
                    Coding(
                        system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                        code=getattr(data, 'form_code',
                                     '[Insert Form Code]')
                    )
                ]
            ),
            amount=Ratio(
                numerator=Quantity(
                    value=20,
                    unit="St",
                    extension=[
                        Extension(
                            url="https://gematik.de/fhir/dev-epa-medication/StructureDefinition/medication-total-quantity-formulation-extension",
                            valueString="20 St."
                        )
                    ]
                ),
                denominator=Quantity(
                    value=1
                )
            )
        )
        return medication
