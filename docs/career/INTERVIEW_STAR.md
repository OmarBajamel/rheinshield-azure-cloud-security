# STAR interview story

## Situation

A fictional German marketplace needed an Azure migration design that security engineers, SOC analysts, auditors, and management could all inspect. The difficult part was connecting architecture, identity, detections, incidents, and German assurance expectations without inventing a live deployment.

## Task

Build a safe, portfolio-grade platform with an enterprise reference, deployable lab, deterministic offline mode, traceable evidence, bilingual communication, and a hard €20 cloud-cost ceiling.

## Action

I translated the BIA and asset inventory into 27 risks and 20 controls; separated the enterprise and lab scopes; composed five Terraform modules and a 14-control policy baseline; modeled Entra Zero Trust and GitHub OIDC; built 14 KQL detections plus hunting/workbook/SOAR content; generated 738 events; investigated INC-001; automated sanitization; and exposed the result in an eight-route React dashboard. Real gates corrected invalid HCL/provider arguments and two accessibility defects before release.

## Result

The final public implementation is reproducible without Azure credentials. Terraform format/init/validate and one native mock test pass; 28/28 detection fixture expectations pass; ten Python tests and four dashboard unit tests pass; browser QA covers eight routes × two languages, mobile layout, zero console errors, and zero axe A/AA violations across three representative scans. Live Azure remains honestly `READY_NOT_AUTHENTICATED`.
