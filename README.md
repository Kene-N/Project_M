# Melian Intelligence System (MVP Database) v1.0.0

An offline-first, local intelligence digital ledger designed to help Nigerian Security Services personnel digitize grassroots operational data, suspect tracking, and case management.

---

## 🚀 Quick Start (Windows)

1. **Download:** Download the `MVP_Database` distribution folder or `DB.zip` from the official repository storage.
2. **Directory Structure:** Keep `mvp_app.exe` in its installation directory alongside the `_internal` and `mvp/assets/` folders. **Do not move `mvp_app.exe` out of its folder.**
3. **Launch:** Double-click `mvp_app.exe` to start the application.
   * *Tip:* Right-click `mvp_app.exe` and select **Send to → Desktop (create shortcut)** for easy access.

---

## 🔑 First-Time Initialization

* On the first launch, the application triggers **System Setup Mode**, prompting you to create the **Master Admin account**.
* *Note:* The system permits a maximum of **3 Admin accounts** per station database instance.

---

## 🔒 Security & Data Privacy (Critical)

* **Local Storage:** All records, case intelligence, mugshots, and system data are saved strictly **locally** inside `mvp.db` and the local `mvp/assets/` folder.
* **Do Not Share Active Databases:** Never share, transmit, or copy your station's populated "MVP Database" folder to unauthorized personnel. Doing so will expose all gathered local intelligence records.
* **Deploying to New Stations/Personnel:** To deploy a clean database instance to another station or officer, direct them to download a fresh, unpopulated "Ground Zero" build from the [Official Downloads Drive Folder](https://drive.google.com/drive/folders/1xdjWPt4NKBLd7_kXpOG8lvxRtgkql-A2?usp=drive_link).
* **Offline-First:** This application operates entirely offline and does not transmit data or telemetry to external cloud servers.

---

## 💾 Data Backup

To perform a manual database backup:
1. Locate the `mvp.db` file in the application directory.
2. Copy `mvp.db` to a secure, encrypted storage device (e.g., an encrypted USB drive).

---

## 🗺️ Product Roadmap

This product is engineered to empower security services personnel with rapid local intelligence capture. 

* **Upcoming Features:**
  * Specialized hardware biometrics integration (e.g., fingerprint scanners).
  * Station Ledger intake module (complaints, patrol logs, and civil disputes).
  * Tiered Role-Based Access Control (Tier 1 Desk, Tier 2 Investigator, Tier 3 Command).
  * Automated migration utilities for local SQLite to central PostgreSQL deployments.
* **Compliance & Access:** The software is free to use for security personnel and adheres to relevant statutory data and security policies to improve local community safety outcomes.

---

## 📩 Feedback & Support

This application is currently in active Beta MVP development. To report bugs, technical errors, crash logs, or suggest new operational data fields:
* **Developer Email:** [kenenwachukwu@gmail.com](mailto:kenenwachukwu@gmail.com)
* **In-Drive Feedback:** Leave notes in the *Comments* document within the deployment Drive folder.
