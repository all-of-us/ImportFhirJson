# Resource Fixes

## Patient
I consider this a base class as it doesn't depend on anything before it. 

## Observation
has a `Subject` Field, with a `Reference` field that will need adjusted
can have an `encounter` field, with a `reference` field that needs adjusted
can have a `performer` field, with a `actor` reference that needs adjusted (can be multiple performers)
can have a `specimin` field, with a `reference` field that needs adjusted
can have a `device` field, with a `reference` field that needs adjusted
can have a `related` field, which may have a `targed` field that needs adjusted
in OMOP, the measurement_date is required, in FHIR it is not. we will have issues importing if it is not in existence

## Medication
can contain Ingredients (which reference other Medications)
We don't utilize medication types

## Condition
has a `patient` field, with a `reference` field that needs adjusted

## Procedure
has a `subject` field, with a `reference` field that needs adjusted
can have a `reason` field, with a `reasonReference` that needs adjusted
can have a `performer` field, with a `actor` reference that needs adjusted (can be multiple performers)
can have an `encounter` field, with a `reference` field that needs adjusted
can have a `location` field, with a `reference` field that needs adjusted
can have a `report` field, with a `reference` field that needs adjusted
can have a `request` field, with a `reference` field that needs adjusted
can have a `focalDrvice` field, with a `maniuplated` field that needs adjusted (can be multiple focalDevices)
can have a `used` field, with a `reference` field that needs adjusted

## Encounter
has `patient` field, with a `reference` field that needs adjusted
has an `indication` field, with multiple `reference` fields that need adjusted (these link to Conditions)

## MedicationStatement
has a `patient` field, with a `reference` field that needs adjusted
can have an `informationSource` field with a `reference` field that needs adjusted
can have a `reasonForUse` field with a `reasonForUseReference` field that needs adjusted
can have a `suppotingInformation` with a `reference` field that needs adjusted (can be multiple supportingInformation)
has a `medication` field, which may have a medicationReference that needs adjusted
may have a `dosage` field, that may have a `site` field which may have a `siteReference` field that needs adjusted

## Practicioner
can have a `practitionerRole` field which may have a `managingOrganization` field, `location` field, `healthcareService` field that all need adjusted
can have a `qualification` field which may have an `issuer` field that needs adjusted

## MedicationOrder
can have a `patient` field, with a `reference` field that needs adjusted
can have a `perscriber` field, with a `reference` field that needs adjusted
can have an `encounter` field, with a `reference` field that needs adjusted
can have a `reason` field with a `reasonReference` field that needs adjusted
has a `medication` field, which may have a medicationReference that needs adjusted
may have a `dosage` field, that may have a `site` field which may have a `siteReference` field that needs adjusted
may have a `dispenseRequest` field, that may have a `medication` field, which may have a medicationReference that needs adjusted
may have a `priorPrescription` field, with a `reference` field that needs adjusted
in OMOP, the drug_exposure_start_date is required, in FHIR it is not. we will have issues importing if it is not in existance. 

## Device
can have an `owner` field, with a `reference` field that needs adjusted
can have an `location` field, with a `reference` field that needs adjusted
can have an `patient` field, with a `reference` field that needs adjusted

note- we don't allow posting of Device directly, you must use DeviceUseStatment

## DeviceUseStatement
can have a `bodySite` field, with a `bodySiteReference` field that needs adjusted
can have a `device` field, with a `reference` field that needs adjusted
has a `subject` field, with a `reference` field that needs adjusted

## DocumentReference
can have a `subject` field, with a `reference` field that needs adjusted
can have an `author` field, with a `reference` field that needs adjusted (can be multiple authors)
can have a `authenticator` field, with a `reference` field that needs adjusted
can have a `relatesTo` field, with a `target` field with a `reference` field that needs adjusted
can have a `context` field, with a `encounter` field with a `reference` field that needs adjusted
can have a `context` field, with a `sourcePatientInfo` field with a `reference` field that needs adjusted
can have a `context` field, with a `related` field with a `ref` field with a `reference` field that needs adjusted (may be multiple related)