# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering
**Problem Statement #11 — Healthcare & Telemedicine**
**Project:** Telemedicine Slot Booking & Prescription Portal

## Overview

A secure healthcare consultation portal that lets remote patients view doctor specialties, book video consultation slots, receive encrypted tele-consultation room links, and download digitally signed prescriptions.

**Actors:** Patient, Attending Physician, Payment Gateway (external system)

## Repository Contents

| File | Description |
|---|---|
| [`Lab1_PES1UG24CS093_B.pdf`](./Lab1_Combined.pdf) | All three deliverables in one file — Requirements Table (p.1), UML Use-Case Diagram (p.2), Use-Case Flow Specification (p.3) |

## Deliverable Details

**Requirements Table**
5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001–NFR-002), each with priority, measurable acceptance criteria, and rationale.

**UML Use-Case Diagram**
3 actors (Patient, Attending Physician, Payment Gateway) and 9 use cases, with:
- `<<include>>` — Book Consultation Slot → Process Payment
- `<<include>>` — Author & Sign Prescription → Validate Physician License
- `<<extend>>` — Cancel / Reschedule Slot → Book Consultation Slot
- `<<extend>>` — Download Prescription PDF → Author & Sign Prescription

**Use-Case Flow Specification**
One-page flow for **UC-03: Book Video Consultation Slot** — preconditions, postconditions, a 10-step main success scenario, and an alternate flow for a declined payment.

## Use-Case Summary

| ID | Use Case | Actor(s) |
|---|---|---|
| UC-01 | Register / Login | Patient, Physician |
| UC-02 | View Doctor Specialties | Patient |
| UC-03 | Book Consultation Slot | Patient |
| UC-04 | Process Payment | Payment Gateway |
| UC-05 | Cancel / Reschedule Slot | Patient |
| UC-06 | Join Video Consultation | Patient, Physician |
| UC-07 | Author & Sign Prescription | Physician |
| UC-08 | Validate Physician License | — |
| UC-09 | Download Prescription PDF | Patient |

## Notes

- FR-001 and NFR-001 were provided in the lab handout; all other requirements were authored for this submission.
- The core use case documented in detail is **UC-03: Book Video Consultation Slot**, since it is the central transaction the rest of the system depends on.
