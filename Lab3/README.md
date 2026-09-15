# Software Engineering Labs — Atharva Ashish Vyas (PES1UG24CS093)

Problem Statement #11: **Telemedicine Slot Booking & Prescription Portal**
Actors: Patient, Attending Physician, Payment Gateway (external system)

This repository contains the lab submissions for the Software Engineering course, all based on the same assigned problem statement.

## Repository Structure

```
SE_Lab1/
├── README.md
├── Lab1/
│   └── Lab1_PES1UG24CS093_B.pdf        # Requirements table + use-case diagram + flow spec
└── Lab3/
    ├── Lab3_ComponentDiagram_Justification_PES1UG24CS093.pdf   # Component diagram + written justification
    └── component_diagram.png / .jpeg    # Standalone diagram image (if included)
```

## Lab 1 — Requirements Engineering & Use-Case Modelling

- **Requirements Table**: 5 functional requirements (FR-001–FR-005) and 2 non-functional requirements (NFR-001, NFR-002) covering prescription signing, slot booking, payment-gated booking, encrypted video links, and prescription retrieval.
- **Use-Case Diagram**: 9 use cases (UC-01–UC-09) across Patient, Attending Physician, and the external Payment Gateway, including `<<include>>` and `<<extend>>` relationships.
- **Use-Case Flow Specification**: Detailed main success scenario and alternate flow for UC-03 (Book Video Consultation Slot), including payment failure handling.

## Lab 3 — Component Modelling & Architectural Pattern Selection

Builds directly on the Lab 1 problem statement.

- **Architectural style selected**: Microservices Architecture.
- **Component Diagram**: API Gateway, Auth & User Service, Appointment Booking Service, Payment Service, Video Session Service, Prescription Service, Notification Service, Appointment Database, Prescription/EHR Database, and the external Payment Gateway — with provided/required interfaces (ball-and-socket notation), `<<include>>` dependency, and a requirement-traceability panel mapping each component back to FR-001–FR-005 and NFR-001–NFR-002.
- **Written Justification**: Explains the choice of Microservices over Layered and Client-Server architectures, with reasoning on independent scaling (video consultations, NFR-002), fault isolation (external Payment Gateway dependency), a security advantage (PHI isolation via the Prescription Service + RBAC at the gateway), and a performance benefit (targeted scaling of the video workload).

## Tools Used

- draw.io — component and use-case diagrams
- Microsoft Word / PDF — requirements table and architectural justification

## Author

Atharva Ashish Vyas
SRN: PES1UG24CS093
