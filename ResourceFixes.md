# Resource Fixes

## Patient


## Observation
has a `Subject` Field, with a `Reference` field that will need adjusted
in OMOP, the measurement_date is required, in FHIR it is not. we will have issues importing if it is not in existance

## Medication
can contain Ingredients (which reference other Medications)
We don't utilize medication types