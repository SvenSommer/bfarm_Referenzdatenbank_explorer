from fhir_profiles.epa_medication_1_0 import EpaMedication1_0

class FHIRProfileFactory:
    SUPPORTED_PROFILES = {
        "epa-medication": ["1.0"]
    }
    
    @staticmethod
    def create(profile, version, data):
        if profile == "epa-medication" and version == "1.0":
            return EpaMedication1_0().create(data)
        else:
            raise ValueError("Unsupported FHIR profile or version")
    
    @staticmethod
    def get_supported_profiles():
        return FHIRProfileFactory.SUPPORTED_PROFILES