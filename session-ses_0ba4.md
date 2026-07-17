#!/usr/bin/env python3
"""SGC TECH AI CPQ — Source Code Scaffold Builder"""
import os

P = "sgc-tech-ai-cpq-src"
dirs = [f"{P}/src/css", f"{P}/src/js", f"{P}/src/data", f"{P}/dist", f"{P}/docs"]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# ═══════════════════════════════════════════════
# src/data/catalogs.js
# ═══════════════════════════════════════════════
open(f"{P}/src/data/catalogs.js","w").write(r"""/**
 * SGC TECH AI — Master Commercial Catalogs
 * All pricing in AED. Blended rate: 425/hr
 */

const BLENDED_RATE = 425;

const products = [
  {cat:"ERP",product:"Odoo",sub:"Sales",desc:"Full sales cycle management with quotations, orders, and invoicing",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:35,ann:378,impl:true,supp:"Bug fixes",rem:"Core module"},
  {cat:"ERP",product:"Odoo",sub:"CRM",desc:"Lead management, pipeline tracking, and sales forecasting",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:"Includes Kanban"},
  {cat:"ERP",product:"Odoo",sub:"Accounting",desc:"Full double-entry accounting, GST/VAT, bank reconciliation",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:40,ann:432,impl:true,supp:"Bug fixes",rem:"UAE VAT compliant"},
  {cat:"ERP",product:"Odoo",sub:"Inventory",desc:"Multi-warehouse inventory with lot/serial tracking",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:35,ann:378,impl:true,supp:"Bug fixes",rem:"Barcode supported"},
  {cat:"ERP",product:"Odoo",sub:"Purchasing",desc:"Purchase orders, vendor management, RFQ process",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"HR",desc:"Employee records, attendance, leave management, recruitment",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Payroll",desc:"Salary computation, WPS compliance, payslip generation",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:35,ann:378,impl:true,supp:"Bug fixes",rem:"UAE WPS ready"},
  {cat:"ERP",product:"Odoo",sub:"Project",desc:"Project planning, task management, timesheets, Gantt charts",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Website Builder",desc:"Drag-and-drop website builder with CMS and blogging",lic:"Subscription",vendor:"Odoo SA",unit:"Site/Mo",mo:50,ann:540,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"E-Commerce",desc:"Online storefront with payment integration and shipping",lic:"Subscription",vendor:"Odoo SA",unit:"Site/Mo",mo:60,ann:648,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Point of Sale",desc:"Restaurant and retail POS with hardware integration",lic:"Subscription",vendor:"Odoo SA",unit:"Terminal/Mo",mo:40,ann:432,impl:true,supp:"Bug fixes",rem:"IoT box supported"},
  {cat:"ERP",product:"Odoo",sub:"Manufacturing",desc:"BOM, work orders, routing, MRP, quality control",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:45,ann:486,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Maintenance",desc:"Equipment maintenance scheduling and work orders",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:25,ann:270,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Fleet",desc:"Vehicle management, fuel logs, contracts, services",lic:"Subscription",vendor:"Odoo SA",unit:"Vehicle/Mo",mo:20,ann:216,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Helpdesk",desc:"Ticket management, SLA tracking, customer support",lic:"Subscription",vendor:"Odoo SA",unit:"Agent/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Field Service",desc:"Field worker scheduling, routing, checklists",lic:"Subscription",vendor:"Odoo SA",unit:"Worker/Mo",mo:35,ann:378,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo",sub:"Marketing",desc:"Email campaigns, marketing automation, analytics",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:30,ann:324,impl:true,supp:"Bug fixes",rem:""},
  {cat:"ERP",product:"Odoo Enterprise",sub:"Full Suite",desc:"Complete Odoo Enterprise with all modules included",lic:"Subscription",vendor:"Odoo SA",unit:"User/Mo",mo:120,ann:1296,impl:true,supp:"Priority",rem:"Best value for 10+ users"},
  {cat:"Microsoft",product:"Microsoft 365",sub:"Business Basic",desc:"Web/mobile Office apps, Teams, OneDrive 1TB",lic:"Subscription",vendor:"Microsoft",unit:"User/Mo",mo:18,ann:216,impl:false,supp:"Microsoft",rem:""},
  {cat:"Microsoft",product:"Microsoft 365",sub:"Business Premium",desc:"Full Office apps, Teams, Intune, Azure AD P1",lic:"Subscription",vendor:"Microsoft",unit:"User/Mo",mo:38,ann:456,impl:true,supp:"Microsoft",rem:"Recommended"},
  {cat:"Microsoft",product:"Power BI",sub:"Pro",desc:"Self-service BI, dashboards, data connectivity",lic:"Subscription",vendor:"Microsoft",unit:"User/Mo",mo:32,ann:384,impl:true,supp:"Microsoft",rem:""},
  {cat:"Microsoft",product:"Power BI",sub:"Premium Per Capacity",desc:"Enterprise BI with dedicated capacity, paginated reports",lic:"Subscription",vendor:"Microsoft",unit:"Capacity/Mo",mo:4995,ann:59940,impl:true,supp:"Microsoft",rem:"P1 tier"},
  {cat:"Microsoft",product:"Dynamics 365",sub:"Sales Enterprise",desc:"Advanced CRM with lead scoring, forecasting, AI insights",lic:"Subscription",vendor:"Microsoft",unit:"User/Mo",mo:95,ann:1140,impl:true,supp:"Microsoft",rem:""},
  {cat:"Microsoft",product:"Azure",sub:"Various",desc:"Cloud infrastructure, AI services, data services",lic:"Pay-as-you-go",vendor:"Microsoft",unit:"Usage",mo:0,ann:0,impl:true,supp:"Microsoft",rem:"Billed separately by Azure"},
  {cat:"AI Solutions",product:"SGC AI Lead Scorer",sub:"Standard",desc:"Rule-based lead scoring with configurable criteria",lic:"SaaS Add-on",vendor:"SGC TECH AI",unit:"Mo",mo:1500,ann:16200,impl:true,supp:"Included",rem:"Tier 1"},
  {cat:"AI Solutions",product:"SGC AI Lead Scorer",sub:"ML Model",desc:"Machine learning lead scoring trained on historical data",lic:"SaaS Add-on",vendor:"SGC TECH AI",unit:"Mo",mo:3500,ann:37800,impl:true,supp:"Included",rem:"Tier 2"},
  {cat:"AI Solutions",product:"SGC AI Lead Scorer",sub:"Predictive",desc:"Predictive lead scoring with real-time behavioral signals",lic:"SaaS Add-on",vendor:"SGC TECH AI",unit:"Mo",mo:6000,ann:64800,impl:true,supp:"Included",rem:"Tier 3"},
  {cat:"AI Solutions",product:"SGC AI Chatbot",sub:"Standard",desc:"FAQ and knowledge base chatbot for customer support",lic:"SaaS Add-on",vendor:"SGC TECH AI",unit:"Mo",mo:2500,ann:27000,impl:true,supp:"Included",rem:""},
  {cat:"AI Solutions",product:"SGC AI Chatbot",sub:"Advanced",desc:"Multi-intent chatbot with CRM integration and handoff",lic:"SaaS Add-on",vendor:"SGC TECH AI",unit:"Mo",mo:5000,ann:54000,impl:true,supp:"Included",rem:""},
  {cat:"AI Solutions",product:"SGC AI Document OCR",sub:"Standard",desc:"Automated document extraction \u2014 invoices, IDs, contracts",lic:"Per-Document",vendor:"SGC TECH AI",unit:"100 docs",mo:200,ann:2400,impl:true,supp:"Included",rem:""},
  {cat:"AI Solutions",product:"SGC AI Predictive Analytics",sub:"Enterprise",desc:"Demand forecasting, churn prediction, revenue modeling",lic:"SaaS",vendor:"SGC TECH AI",unit:"Mo",mo:8000,ann:86400,impl:true,supp:"Dedicated",rem:""},
  {cat:"Infrastructure",product:"SGC Cloud Hosting",sub:"Foundation",desc:"Managed Odoo hosting \u2014 2 vCPU, 4GB RAM, 50GB SSD",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:2800,ann:33600,impl:false,supp:"24/7 Monitoring",rem:"Up to 20 users"},
  {cat:"Infrastructure",product:"SGC Cloud Hosting",sub:"Growth",desc:"Managed Odoo hosting \u2014 4 vCPU, 8GB RAM, 100GB SSD",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:4200,ann:50400,impl:false,supp:"24/7 Monitoring",rem:"Up to 50 users"},
  {cat:"Infrastructure",product:"SGC Cloud Hosting",sub:"Enterprise",desc:"Managed Odoo hosting \u2014 8 vCPU, 16GB RAM, 200GB SSD, HA",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:5600,ann:67200,impl:false,supp:"24/7 Dedicated",rem:"Unlimited users"},
  {cat:"Infrastructure",product:"AWS Hosting",sub:"EC2 t3.medium",desc:"AWS EC2 instance \u2014 2 vCPU, 4GB RAM, UAE region",lic:"Pay-as-you-go",vendor:"AWS",unit:"Mo",mo:120,ann:1440,impl:true,supp:"AWS",rem:"Billed by AWS"},
  {cat:"Infrastructure",product:"AWS Hosting",sub:"EC2 r6g.large",desc:"AWS EC2 instance \u2014 2 vCPU, 16GB RAM, UAE region",lic:"Pay-as-you-go",vendor:"AWS",unit:"Mo",mo:350,ann:4200,impl:true,supp:"AWS",rem:"Billed by AWS"},
  {cat:"Cybersecurity",product:"Penetration Testing",sub:"Web App",desc:"OWASP Top 10 penetration test with full report",lic:"One-time",vendor:"SGC TECH AI",unit:"Per test",mo:0,ann:15000,impl:false,supp:"Re-test",rem:"5-7 day engagement"},
  {cat:"Cybersecurity",product:"Security Audit",sub:"Infrastructure",desc:"Cloud infrastructure security assessment and hardening",lic:"One-time",vendor:"SGC TECH AI",unit:"Per audit",mo:0,ann:25000,impl:false,supp:"Report",rem:""},
  {cat:"Cybersecurity",product:"Compliance",sub:"PDPL Assessment",desc:"UAE Personal Data Protection Law compliance gap analysis",lic:"One-time",vendor:"SGC TECH AI",unit:"Per assessment",mo:0,ann:35000,impl:false,supp:"Report",rem:""},
  {cat:"Training",product:"End User Training",sub:"Standard",desc:"Group training sessions for end users \u2014 up to 15 attendees",lic:"Per session",vendor:"SGC TECH AI",unit:"Session",mo:0,ann:2125,impl:false,supp:"Materials",rem:"5 hours"},
  {cat:"Training",product:"Admin Training",sub:"Advanced",desc:"System administrator deep-dive \u2014 configuration, workflows",lic:"Per session",vendor:"SGC TECH AI",unit:"Session",mo:0,ann:3250,impl:false,supp:"Materials",rem:"5 hours"},
  {cat:"Training",product:"Executive Workshop",sub:"Strategy",desc:"C-suite workshop on platform capabilities and roadmap",lic:"Per session",vendor:"SGC TECH AI",unit:"Session",mo:0,ann:4250,impl:false,supp:"Materials",rem:"4 hours"},
  {cat:"Support",product:"SGC Support",sub:"Email",desc:"Business-hour email support, 24hr response SLA",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:800,ann:9600,impl:false,supp:"Included",rem:"Tier 1"},
  {cat:"Support",product:"SGC Support",sub:"Priority",desc:"Priority email + phone, 4hr response SLA, bug fixes",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:2000,ann:24000,impl:false,supp:"Included",rem:"Tier 2"},
  {cat:"Support",product:"SGC Support",sub:"Dedicated 24/7",desc:"Dedicated team, 1hr response, 24/7 coverage, SLA guarantees",lic:"Subscription",vendor:"SGC TECH AI",unit:"Mo",mo:4500,ann:54000,impl:false,supp:"Included",rem:"Tier 3"},
];

const services = [
  {svc:"Discovery Workshop",mod:"All",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Discovery",consult:"Business Analyst",dep:"None",del:"Requirements Document, Scope Definition"},
  {svc:"Requirements Mapping",mod:"All",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Discovery",consult:"Business Analyst",dep:"Discovery Workshop",del:"Functional Requirements Spec, Process Maps"},
  {svc:"As-Is Process Audit",mod:"All",cpx:"Medium",hrs:12,rate:BLENDED_RATE,cat:"Discovery",consult:"Senior Consultant",dep:"None",del:"Current State Document, Gap Analysis"},
  {svc:"Solution Architecture",mod:"All",cpx:"Complex",hrs:24,rate:750,cat:"Discovery",consult:"Solution Architect",dep:"Requirements Mapping",del:"Architecture Document, Tech Stack Decision"},
  {svc:"CRM Configuration",mod:"CRM",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Configured CRM Module"},
  {svc:"CRM Configuration",mod:"CRM",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"CRM with Custom Fields, Pipelines"},
  {svc:"CRM Configuration",mod:"CRM",cpx:"Complex",hrs:32,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Requirements",del:"Full CRM with Automation, Scoring"},
  {svc:"Sales Module Setup",mod:"Sales",cpx:"Simple",hrs:6,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Configured Sales Module"},
  {svc:"Sales Module Setup",mod:"Sales",cpx:"Medium",hrs:12,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Sales with Pricelists, Templates"},
  {svc:"Accounting Setup",mod:"Accounting",cpx:"Simple",hrs:10,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Chart of Accounts",del:"Configured Accounting, Journal Entries"},
  {svc:"Accounting Setup",mod:"Accounting",cpx:"Medium",hrs:20,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Chart of Accounts",del:"Full Accounting with VAT, Reconciliation"},
  {svc:"Accounting Setup",mod:"Accounting",cpx:"Complex",hrs:40,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Requirements",del:"Multi-company Accounting, Consolidation"},
  {svc:"Inventory Setup",mod:"Inventory",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Single Warehouse Config"},
  {svc:"Inventory Setup",mod:"Inventory",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Multi-warehouse, Routes, Reordering Rules"},
  {svc:"Inventory Setup",mod:"Inventory",cpx:"Complex",hrs:32,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Requirements",del:"Full WMS with Barcode, Lot/Serial"},
  {svc:"HR Module Setup",mod:"HR",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Employee Records, Departments"},
  {svc:"HR Module Setup",mod:"HR",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"HR with Leave, Attendance, Recruitment"},
  {svc:"Payroll Setup",mod:"Payroll",cpx:"Medium",hrs:20,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"HR Setup",del:"Payroll Rules, WPS File, Payslips"},
  {svc:"Payroll Setup",mod:"Payroll",cpx:"Complex",hrs:40,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"HR Setup",del:"Complex Payroll with Overtime, Allowances, EOS"},
  {svc:"Project Module Setup",mod:"Project",cpx:"Simple",hrs:6,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Project Stages, Task Templates"},
  {svc:"Project Module Setup",mod:"Project",cpx:"Medium",hrs:14,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Requirements",del:"Projects with Timesheets, Billing"},
  {svc:"E-Commerce Setup",mod:"E-Commerce",cpx:"Medium",hrs:24,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Website, Products",del:"Online Store with Payments, Shipping"},
  {svc:"POS Setup",mod:"POS",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Products, Pricing",del:"Configured POS with Barcodes"},
  {svc:"POS Setup",mod:"POS",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Products, Pricing",del:"POS with Restaurant Mode, Kitchen Display"},
  {svc:"Manufacturing Setup",mod:"Manufacturing",cpx:"Medium",hrs:24,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Products, BOM",del:"BOMs, Work Orders, Routing"},
  {svc:"Manufacturing Setup",mod:"Manufacturing",cpx:"Complex",hrs:48,rate:BLENDED_RATE,cat:"Configuration",consult:"Technical Lead",dep:"Products, BOM",del:"Full MRP with Quality, Maintenance"},
  {svc:"Portal Integration",mod:"Portal",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Module Setup",del:"Customer/Vendor Portal"},
  {svc:"Portal Integration",mod:"Portal",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Module Setup",del:"Portal with Custom Pages, Forms"},
  {svc:"Report Configuration",mod:"All",cpx:"Simple",hrs:4,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Module Setup",del:"Standard Report Configuration"},
  {svc:"Report Configuration",mod:"All",cpx:"Medium",hrs:10,rate:BLENDED_RATE,cat:"Configuration",consult:"Consultant",dep:"Module Setup",del:"Custom QWeb Reports"},
  {svc:"Report Configuration",mod:"All",cpx:"Complex",hrs:24,rate:BLENDED_RATE,cat:"Configuration",consult:"Senior Consultant",dep:"Module Setup",del:"Complex Reports with Sub-reports, Charts"},
  {svc:"Data Migration",mod:"All",cpx:"Simple",hrs:12,rate:BLENDED_RATE,cat:"Migration",consult:"Consultant",dep:"Templates, Mapping",del:"Migrated Data, Validation Report"},
  {svc:"Data Migration",mod:"All",cpx:"Medium",hrs:30,rate:BLENDED_RATE,cat:"Migration",consult:"Senior Consultant",dep:"Templates, Mapping",del:"Migrated Data with Transformation, Validation"},
  {svc:"Data Migration",mod:"All",cpx:"Complex",hrs:60,rate:BLENDED_RATE,cat:"Migration",consult:"Technical Lead",dep:"Templates, Mapping",del:"Complex Migration with Reconciliation"},
  {svc:"User Training",mod:"All",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Training",consult:"Trainer",dep:"Configuration Complete",del:"Training Materials, Session Delivery"},
  {svc:"User Training",mod:"All",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Training",consult:"Trainer",dep:"Configuration Complete",del:"Multi-role Training, Videos, Manuals"},
  {svc:"User Training",mod:"All",cpx:"Complex",hrs:32,rate:BLENDED_RATE,cat:"Training",consult:"Trainer",dep:"Configuration Complete",del:"Comprehensive Training Program"},
  {svc:"Go-Live Support",mod:"All",cpx:"Simple",hrs:8,rate:BLENDED_RATE,cat:"Go-Live",consult:"Consultant",dep:"UAT Sign-off",del:"Go-Live Monitoring, Issue Resolution"},
  {svc:"Go-Live Support",mod:"All",cpx:"Medium",hrs:16,rate:BLENDED_RATE,cat:"Go-Live",consult:"Senior Consultant",dep:"UAT Sign-off",del:"Extended Go-Live with Hypercare"},
  {svc:"Portal API Integration",mod:"Integration",cpx:"Medium",hrs:24,rate:BLENDED_RATE,cat:"Integration",consult:"Developer",dep:"Portal Access",del:"API Integration, Lead Sync"},
  {svc:"WhatsApp Business API",mod:"Integration",cpx:"Medium",hrs:32,rate:BLENDED_RATE,cat:"Integration",consult:"Developer",dep:"WhatsApp Account",del:"WhatsApp Integration, Templates"},
  {svc:"Payment Gateway",mod:"Integration",cpx:"Simple",hrs:12,rate:BLENDED_RATE,cat:"Integration",consult:"Developer",dep:"Gateway Account",del:"Payment Integration, Testing"},
  {svc:"Power BI Connector",mod:"Integration",cpx:"Medium",hrs:20,rate:BLENDED_RATE,cat:"Integration",consult:"Data Engineer",dep:"Data Model",del:"Power BI Dashboard, Data Pipeline"},
  {svc:"REST API Development",mod:"Integration",cpx:"Medium",hrs:32,rate:BLENDED_RATE,cat:"Integration",consult:"Developer",dep:"Architecture",del:"API Endpoints, Documentation"},
  {svc:"Third-Party API Integration",mod:"Integration",cpx:"Simple",hrs:12,rate:BLENDED_RATE,cat:"Integration",consult:"Developer",dep:"API Access",del:"Integration, Error Handling"},
  {svc:"Multi-Channel Sync",mod:"Integration",cpx:"Complex",hrs:48,rate:BLENDED_RATE,cat:"Integration",consult:"Senior Developer",dep:"Architecture",del:"Omnichannel Data Sync Engine"},
];

const devCatalog = [
  {feat:"Custom Dashboard",desc:"Executive KPI dashboard with real-time data widgets and drill-down",diff:"Simple",devHrs:24,devLvl:"Developer",testHrs:6,docHrs:4,pmHrs:4},
  {feat:"Custom Workflow",desc:"Multi-step approval workflow with conditional routing and notifications",diff:"Simple",devHrs:24,devLvl:"Developer",testHrs:6,docHrs:4,pmHrs:4},
  {feat:"WhatsApp Integration",desc:"Two-way WhatsApp messaging with template management and media support",diff:"Medium",devHrs:48,devLvl:"Senior Developer",testHrs:12,docHrs:6,pmHrs:6},
  {feat:"REST API",desc:"Custom REST API endpoints with authentication, rate limiting, and documentation",diff:"Medium",devHrs:40,devLvl:"Senior Developer",testHrs:10,docHrs:8,pmHrs:6},
  {feat:"Power BI Connector",desc:"DirectQuery or import connector for Power BI with data model",diff:"Medium",devHrs:32,devLvl:"Data Engineer",testHrs:8,docHrs:6,pmHrs:4},
  {feat:"AI Chatbot",desc:"Conversational AI chatbot with NLU, context retention, and CRM integration",diff:"Complex",devHrs:80,devLvl:"AI Engineer",testHrs:20,docHrs:12,pmHrs:10},
  {feat:"Mobile App",desc:"Cross-platform mobile app (iOS/Android) with offline support",diff:"Enterprise",devHrs:160,devLvl:"Senior Developer",testHrs:40,docHrs:20,pmHrs:16},
  {feat:"Approval Workflow",desc:"Multi-level approval matrix with delegation, escalation, and audit trail",diff:"Simple",devHrs:20,devLvl:"Developer",testHrs:6,docHrs:4,pmHrs:4},
  {feat:"Document OCR",desc:"AI-powered document extraction with classification and validation",diff:"Complex",devHrs:80,devLvl:"AI Engineer",testHrs:20,docHrs:10,pmHrs:8},
  {feat:"IoT Integration",desc:"IoT device data ingestion, processing pipeline, and monitoring dashboard",diff:"Complex",devHrs:80,devLvl:"Senior Developer",testHrs:16,docHrs:10,pmHrs:8},
  {feat:"GPS Integration",desc:"Real-time GPS tracking with geofencing, route history, and distance calculation",diff:"Medium",devHrs:40,devLvl:"Developer",testHrs:10,docHrs:6,pmHrs:6},
  {feat:"Biometric Integration",desc:"Fingerprint/face recognition integration for attendance and access control",diff:"Medium",devHrs:40,devLvl:"Senior Developer",testHrs:10,docHrs:6,pmHrs:6},
  {feat:"Payroll Customization",desc:"Custom salary components, overtime rules, EOS calculations per UAE law",diff:"Complex",devHrs:60,devLvl:"Senior Developer",testHrs:16,docHrs:8,pmHrs:8},
  {feat:"Customer Portal",desc:"Self-service portal with order tracking, invoices, support tickets, and payments",diff:"Complex",devHrs:80,devLvl:"Senior Developer",testHrs:20,docHrs:12,pmHrs:10},
  {feat:"Vendor Portal",desc:"Vendor self-service for PO management, invoicing, delivery tracking",diff:"Complex",devHrs:72,devLvl:"Senior Developer",testHrs:18,docHrs:10,pmHrs:8},
  {feat:"Employee Portal",desc:"HR self-service for leave requests, payslips, documents, and declarations",diff:"Medium",devHrs:48,devLvl:"Developer",testHrs:12,docHrs:8,pmHrs:6},
  {feat:"Custom Report Engine",desc:"Ad-hoc report builder with drag-and-drop fields, filters, and scheduling",diff:"Complex",devHrs:64,devLvl:"Senior Developer",testHrs:16,docHrs:10,pmHrs:8},
  {feat:"EDI Integration",desc:"Electronic Data Interchange for B2B document exchange",diff:"Complex",devHrs:80,devLvl:"Senior Developer",testHrs:20,docHrs:12,pmHrs:8},
];

const aiSolutions = [
  {name:"AI Lead Scoring \u2014 Rule-Based",desc:"Configurable rule engine scoring leads by source, demographics, and behavior",tier:"Basic Assistant",hrs:40,rate:850,cat:"Sales AI",del:"Scoring Engine, Configuration UI, Score Field"},
  {name:"AI Lead Scoring \u2014 ML Model",desc:"Machine learning model trained on historical conversion data",tier:"Chatbot",hrs:80,rate:850,cat:"Sales AI",del:"Trained Model, Feature Pipeline, Retraining Job"},
  {name:"AI Lead Scoring \u2014 Predictive",desc:"Real-time predictive scoring with behavioral signals and A/B testing",tier:"Predictive AI",hrs:180,rate:850,cat:"Sales AI",del:"Predictive Model, Real-time API, A/B Framework"},
  {name:"AI Customer Support Chatbot",desc:"NLU-powered chatbot for FAQ, ticket creation, and knowledge base search",tier:"Chatbot",hrs:80,rate:850,cat:"Service AI",del:"Chatbot Widget, Intent Model, Handoff Protocol"},
  {name:"AI Sales Assistant Chatbot",desc:"Conversational AI that qualifies leads, schedules meetings, recommends products",tier:"Chatbot",hrs:100,rate:850,cat:"Sales AI",del:"Sales Bot, Lead Qualification Flow, Calendar Integration"},
  {name:"AI Document Processing",desc:"Automated extraction from invoices, contracts, IDs with validation",tier:"AI Automation",hrs:120,rate:850,cat:"Operations AI",del:"OCR Pipeline, Extraction Models, Validation Rules"},
  {name:"AI Demand Forecasting",desc:"Time-series forecasting for inventory and procurement planning",tier:"Predictive AI",hrs:180,rate:850,cat:"Supply Chain AI",del:"Forecasting Model, Dashboard, Replenishment Rules"},
  {name:"AI Churn Prediction",desc:"Customer churn risk scoring with intervention recommendations",tier:"Predictive AI",hrs:160,rate:850,cat:"Customer AI",del:"Churn Model, Risk Dashboard, Retention Playbooks"},
  {name:"AI Automation Platform",desc:"End-to-end AI workflow automation with human-in-the-loop approval",tier:"AI Automation",hrs:120,rate:850,cat:"Platform AI",del:"Automation Engine, Workflow Designer, Audit Trail"},
  {name:"AI Computer Vision \u2014 QC",desc:"Manufacturing quality control via image classification and defect detection",tier:"Enterprise AI",hrs:300,rate:850,cat:"Manufacturing AI",del:"CV Model, Camera Integration, QC Dashboard"},
  {name:"AI NLP \u2014 Contract Analysis",desc:"Automated contract review with clause extraction, risk flagging, and comparison",tier:"Enterprise AI",hrs:280,rate:850,cat:"Legal AI",del:"NLP Pipeline, Clause Library, Risk Report"},
];

const tierFeatures = [
  {feat:"Lead Capture \u2014 Portal Sync",t1:"Included",t2:"Included",t3:"Included"},
  {feat:"Lead Capture \u2014 Meta & Google",t1:"Not Included",t2:"Included",t3:"Included"},
  {feat:"Lead Capture \u2014 Multi-Channel",t1:"Not Included",t2:"Not Included",t3:"Included"},
  {feat:"CRM & Pipeline Management",t1:"Included",t2:"Included",t3:"Included"},
  {feat:"Agent Accountability & SLA",t1:"Included",t2:"Included",t3:"Included"},
  {feat:"AI Lead Scoring",t1:"Rule-Based",t2:"ML Model",t3:"Predictive"},
  {feat:"Reporting & Dashboards",t1:"Standard",t2:"Advanced",t3:"Executive"},
  {feat:"Automation Workflows",t1:"Not Included",t2:"Included",t3:"Advanced"},
  {feat:"Custom Integrations",t1:"Not Included",t2:"Not Included",t3:"Included"},
  {feat:"WhatsApp Business API",t1:"Not Included",t2:"Included",t3:"Full Suite"},
  {feat:"Website/SEO",t1:"Not Included",t2:"Audit Only",t3:"Audit + Fixes"},
  {feat:"Client/Investor Portal",t1:"Not Included",t2:"Not Included",t3:"Included"},
  {feat:"Penetration Testing",t1:"Not Included",t2:"Not Included",t3:"Included"},
  {feat:"Data Migration",t1:"Basic",t2:"Standard",t3:"Comprehensive"},
  {feat:"User Training",t1:"Basic",t2:"Intermediate",t3:"Advanced"},
  {feat:"Documentation",t1:"Standard",t2:"Extended",t3:"Full Library"},
  {feat:"Support Level",t1:"Email",t2:"Priority",t3:"24/7 Dedicated"},
  {feat:"SLA Response Time",t1:"24 hours",t2:"4 hours",t3:"1 hour"},
  {feat:"Dedicated Project Manager",t1:"Shared",t2:"Dedicated",t3:"Dedicated"},
  {feat:"UAT Environment",t1:"Not Included",t2:"Included",t3:"Included"},
  {feat:"Multi-Branch Support",t1:"Not Included",t2:"Optional",t3:"Included"},
  {feat:"Multi-Currency",t1:"AED Only",t2:"Included",t3:"Included"},
  {feat:"Multi-Language (AR/EN)",t1:"Not Included",t2:"Optional",t3:"Included"},
  {feat:"Custom Report Builder",t1:"Not Included",t2:"Not Included",t3:"Included"},
  {feat:"Executive Mobile App",t1:"Not Included",t2:"Not Included",t3:"Optional"},
  {feat:"Group Company Roadmap",t1:"Not Included",t2:"Not Included",t3:"Forward-Looking"},
];

const industries = [
  {name:"Construction",mods:["Sales","CRM","Project","Inventory","Accounting","HR","Fleet","Maintenance"],ints:["GPS Integration","Biometric","Custom Dashboard","Approval Workflow"],users:"30-100",hrs:280,tier:"Growth"},
  {name:"Manufacturing",mods:["Sales","CRM","Inventory","Manufacturing","Purchase","Accounting","HR","Maintenance"],ints:["IoT Integration","Custom Dashboard","Power BI Connector","Approval Workflow"],users:"40-150",hrs:360,tier:"Enterprise"},
  {name:"Healthcare",mods:["CRM","Accounting","Inventory","HR","Helpdesk"],ints:["Custom Dashboard","WhatsApp Integration","Customer Portal","Document OCR"],users:"50-200",hrs:320,tier:"Enterprise"},
  {name:"Education",mods:["Sales","CRM","Accounting","HR","Payroll","Website","E-Commerce"],ints:["Employee Portal","Custom Workflow","WhatsApp Integration","Payment Gateway"],users:"20-80",hrs:240,tier:"Growth"},
  {name:"Trading",mods:["Sales","CRM","Inventory","Purchase","Accounting","E-Commerce","POS"],ints:["Custom Dashboard","Power BI Connector","REST API","Multi-Channel Sync"],users:"20-60",hrs:260,tier:"Growth"},
  {name:"Retail",mods:["Sales","POS","Inventory","E-Commerce","Accounting","HR","Marketing"],ints:["Payment Gateway","Custom Dashboard","WhatsApp Integration"],users:"30-100",hrs:280,tier:"Growth"},
  {name:"Real Estate",mods:["CRM","Sales","Accounting","Website","Marketing"],ints:["Portal API (Bayut/Property Finder)","WhatsApp Integration","AI Lead Scoring","Custom Dashboard"],users:"10-50",hrs:190,tier:"Foundation"},
  {name:"Hospitality",mods:["Sales","POS","Inventory","Accounting","HR","Payroll","Website","E-Commerce"],ints:["Payment Gateway","Custom Dashboard"],users:"40-200",hrs:340,tier:"Enterprise"},
  {name:"Government",mods:["CRM","Project","Accounting","HR","Payroll","Helpdesk","Fleet","Maintenance"],ints:["Custom Workflow","Approval Workflow","Biometric","Document OCR","Customer Portal"],users:"100-500",hrs:500,tier:"Enterprise"},
  {name:"NGO",mods:["CRM","Accounting","HR","Project","Website","Helpdesk"],ints:["Customer Portal","Custom Workflow","Custom Report Engine","WhatsApp Integration"],users:"15-50",hrs:200,tier:"Foundation"},
  {name:"Logistics",mods:["Sales","CRM","Inventory","Fleet","Maintenance","Accounting","HR","Helpdesk"],ints:["GPS Integration","Custom Dashboard","IoT Integration","Mobile App","REST API"],users:"30-120",hrs:340,tier:"Enterprise"},
];

const rateCard = [
  {role:"Consultant",rate:425,level:"L1"},{role:"Senior Consultant",rate:550,level:"L2"},
  {role:"Project Manager",rate:650,level:"L2"},{role:"Solution Architect",rate:750,level:"L3"},
  {role:"Technical Lead",rate:850,level:"L3"},{role:"Developer",rate:500,level:"L1"},
  {role:"Senior Developer",rate:650,level:"L2"},{role:"AI Engineer",rate:850,level:"L3"},
  {role:"Data Engineer",rate:700,level:"L2"},{role:"Business Analyst",rate:500,level:"L1"},
  {role:"QA Engineer",rate:450,level:"L1"},{role:"Trainer",rate:425,level:"L1"},
];

const commercialRules = [
  "Implementation is always calculated before discount. The full effort-based price is determined first, then discount is applied as a separate line item.",
  "Discount never changes estimated hours. Hours represent genuine effort and remain fixed regardless of commercial negotiations.",
  "Hours must remain auditable. Every hour in a proposal must trace to a specific task, module, and complexity level in the service catalog.",
  "Every custom feature must have documentation hours. No development item is delivered without corresponding documentation.",
  "Every development includes QA. Testing hours are non-negotiable and calculated as a percentage of development effort.",
  "Every implementation includes PM hours. Project Management at 15% is a mandatory line item, never waived.",
  "Every proposal must include assumptions. Assumptions protect both SGC and the client from scope ambiguity.",
  "Every proposal must include exclusions. Explicit exclusions prevent expectation gaps and scope creep.",
  "Every proposal must generate a professional quotation. The commercial summary must be formatted as a standalone document.",
  "Every proposal must generate a commercial summary. A one-page financial overview must accompany every proposal.",
];

const calculatorModules = ["Sales","CRM","Accounting","Inventory","Purchase","HR","Payroll","Project","Website","E-Commerce","POS","Manufacturing","Maintenance","Fleet","Helpdesk","Field Service","Marketing"];
const calculatorCustomizations = ["Custom Dashboard","Custom Workflow","Approval Workflow","Payroll Customization","Custom Report Engine","Multi-Language AR/EN"];
const calculatorIntegrations = ["Portal API (Bayut/Property Finder)","WhatsApp Business API","Payment Gateway","Power BI Connector","REST API","GPS Integration","Biometric Integration","IoT Integration","Document OCR","Mobile App"];
const integrationHours = {"Portal API (Bayut/Property Finder)":24,"WhatsApp Business API":32,"Payment Gateway":12,"Power BI Connector":20,"REST API":32,"GPS Integration":40,"Biometric Integration":40,"IoT Integration":80,"Document OCR":80,"Mobile App":160};
""")

print("  [1/8] src/data/catalogs.js")

# ═══════════════════════════════════════════════
# src/css/brand.css
# ═══════════════════════════════════════════════
open(f"{P}/src/css/brand.css","w").write("""/**
 * SGC TECH AI Brand Design System v3.0
 * Navy #0F213D  Ivory #F7F4EE  Gold #B79554  Charcoal #1C2430
 * IBM Plex Serif (headings)  IBM Plex Sans (body)  IBM Plex Mono (data)
 */
:root{--ivory:#F7F4EE;--navy:#0F213D;--gold:#B79554;--charcoal:#1C2430;--slate:#5F6775;--champagne:#D9C08A;--parchment:#ECE7DF;--midnight:#091528;--emerald:#2C6654;--amber:#C78F2B;--wine:#A24949;--sw:272px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'IBM Plex Sans',sans-serif;background:var(--ivory);color:var(--charcoal);overflow-x:hidden}
h1,h2,h3,.serif{font-family:'IBM Plex Serif',serif}
.mono{font-family:'IBM Plex Mono',monospace}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:var(--parchment)}::-webkit-scrollbar-thumb{background:var(--champagne);border-radius:3px}
#sidebar{position:fixed;left:0;top:0;width:var(--sw);height:100vh;background:var(--navy);z-index:100;display:flex;flex-direction:column;transition:transform .3s ease}
#sidebar .logo-area{padding:24px 20px 16px;border-bottom:1px solid rgba(183,149,84,.15)}
#sidebar .logo-text{font-family:'IBM Plex Serif',serif;font-size:20px;font-weight:700;color:#fff;letter-spacing:-.5px}
#sidebar .logo-sub{font-size:10px;color:var(--gold);letter-spacing:2px;text-transform:uppercase;margin-top:2px}
#sidebar nav{flex:1;overflow-y:auto;padding:12px 0}
#sidebar .nav-group{padding:0 12px;margin-bottom:8px}
#sidebar .nav-label{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(183,149,84,.5);padding:8px 12px 4px;font-weight:600}
#sidebar .nav-item{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:6px;color:rgba(255,255,255,.6);font-size:13px;font-weight:500;cursor:pointer;transition:all .2s;user-select:none}
#sidebar .nav-item:hover{background:rgba(183,149,84,.08);color:rgba(255,255,255,.9)}
#sidebar .nav-item.active{background:rgba(183,149,84,.15);color:var(--gold)}
#sidebar .nav-item svg{width:16px;height:16px;flex-shrink:0}
#sidebar .sidebar-footer{padding:16px 20px;border-top:1px solid rgba(183,149,84,.15)}
#sidebar .coord{font-family:'IBM Plex Mono',monospace;font-size:8px;color:rgba(183,149,84,.25);letter-spacing:.5px}
#main{margin-left:var(--sw);min-height:100vh;position:relative}
#main::before{content:'';position:fixed;top:16px;right:16px;width:60px;height:60px;border-top:.5px solid rgba(183,149,84,.35);border-right:.5px solid rgba(183,149,84,.35);pointer-events:none;z-index:50}
#main::after{content:'';position:fixed;bottom:16px;left:calc(var(--sw) + 16px);width:40px;height:40px;border-bottom:.3px solid rgba(183,149,84,.2);border-left:.3px solid rgba(183,149,84,.2);pointer-events:none;z-index:50}
.watermark-bg{position:fixed;top:0;left:var(--sw);right:0;bottom:0;opacity:.015;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23B79554' stroke-width='.5'%3E%3Cpath d='M0 40h80M40 0v80M0 0l80 80M80 0L0 80'/%3E%3Ccircle cx='40' cy='40' r='20'/%3E%3Ccircle cx='40' cy='40' r='10'/%3E%3C/g%3E%3C/svg%3E");background-size:80px 80px}
.topbar{position:sticky;top:0;z-index:40;background:rgba(247,244,238,.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(183,149,84,.12);padding:16px 32px;display:flex;align-items:center;justify-content:space-between}
.topbar h1{font-size:22px;font-weight:700;color:var(--navy);letter-spacing:-.5px}
.topbar .actions{display:flex;gap:8px}
.section{display:none;padding:28px 32px 48px;position:relative;z-index:1}
.section.active{display:block;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.kpi-card{background:#fff;border:1px solid rgba(183,149,84,.1);border-radius:8px;padding:20px 24px;position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(15,33,61,.06)}
.kpi-card .kpi-label{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--slate);font-weight:600}
.kpi-card .kpi-value{font-family:'IBM Plex Serif',serif;font-size:32px;font-weight:700;color:var(--navy);margin:6px 0 2px}
.kpi-card .kpi-change{font-size:12px;font-weight:500}
.kpi-card .kpi-gold{position:absolute;top:0;right:0;width:4px;height:100%;background:var(--gold);border-radius:0 8px 8px 0}
.live-dot{width:6px;height:6px;background:var(--gold);border-radius:50%;animation:pulseGold 2s infinite}
@keyframes pulseGold{0%,100%{opacity:.6}50%{opacity:1}}
@media(max-width:1024px){#sidebar{transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#main{margin-left:0}.cg{grid-template-columns:1fr}.mt{display:flex!important}}
@media(max-width:640px){.section{padding:20px 16px 40px}.topbar{padding:12px 16px}.pb{padding:32px 24px}.pc{padding:48px 24px}.sb2{grid-template-columns:1fr}}
@media print{#sidebar,.topbar,.watermark-bg,.no-print{display:none!important}#main{margin-left:0!important}#main::before,#main::after{display:none}.section{display:block!important;padding:0!important}.pd{box-shadow:none;border:none}.pc{border-radius:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}table.s thead{background:var(--navy)!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}body{background:#fff}}
""")
print("  [2/8] src/css/brand.css")

# ═══════════════════════════════════════════════
# src/css/components.css + src/js/* + src/index.html
# ═══════════════════════════════════════════════
# These are the files from the previous working build.
# Since the single-file version already works, we extract it and split.

import subprocess, shutil

# The previous tar already has a working single-file build.
# We extract it, read it, and split into the multi-file scaffold.

prev_tar = "sgc-tech-ai-cpq.tar.gz"
if os.path.exists(prev_tar):
    subprocess.run(["tar","xzf",prev_tar,"sgc-tech-ai-cpq/dist/index.html"], check=True)
    src_html = open("sgc-tech-ai-cpq/dist/index.html").read()

    # Extract CSS from the <style> block
    import re
    style_match = re.search(r'<style>(.*?)</style>', src_html, re.DOTALL)
    if style_match:
        all_css = style_match.group(1)
        # Split into brand (first 2000 chars approx) and components (rest)
        # For simplicity, put it all in components since brand.css is mostly in the first part
        # The actual split happened in the previous script - here we just reference the working code
        open(f"{P}/src/css/components.css","w").write(all_css)

    # Extract JS from the <script> block  
    js_match = re.search(r'<script>(.*?)</script>', src_html, re.DOTALL)
    if js_match:
        all_js = js_match.group(1)
        open(f"{P}/src/js/bundle.js","w").write(all_js)
    
    # Create a simple index.html that loads the bundle
    # (The full split version with separate JS files is below)
    
    shutil.rmtree("sgc-tech-ai-cpq", ignore_errors=True)
else:
    print("  Previous tar not found, generating from templates...")

# Now write the proper multi-file JS modules
# We already have the full content in the Python script above for catalogs.js
# The remaining JS files need to be written with proper function signatures

# ═══════════════════════════════════════════════
# src/js/utils.js
# ═══════════════════════════════════════════════
open(f"{P}/src/js/utils.js","w").write("""function fmtNum(n){return n.toLocaleString('en-AE')}
function fmtAED(n){return 'AED '+fmtNum(n)}
function showToast(msg){const t=document.getElementById('toast');document.getElementById('tmsg').textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3000)}
function goToSection(id){document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));const s=document.getElementById('sec-'+id);if(s)s.classList.add('active');const n=document.querySelector('.nav-item[data-sec="'+id+'"]');if(n)n.classList.add('active');document.getElementById('pt').textContent=PAGE_TITLES[id]||id;document.getElementById('sidebar').classList.remove('open');window.scrollTo({top:0,behavior:'smooth'})}
""")
print("  [3/8] src/js/utils.js")

# ═══════════════════════════════════════════════
# src/js/tables.js
# ═══════════════════════════════════════════════
open(f"{P}/src/js/tables.js","w").write("""let sortState={};
function renderTable(containerId,data,cols){
  const w=document.getElementById(containerId);if(!w)return;const key=containerId;if(!sortState[key])sortState[key]={col:-1,asc:true};
  const fi='f-'+containerId;let fd=data;const fe=document.getElementById(fi);
  if(fe&&fe.value){const q=fe.value.toLowerCase();fd=data.filter(r=>cols.some(c=>String(r[c.k]||'').toLowerCase().includes(q)))}
  const s=sortState[key];
  if(s.col>=0){const ck=cols[s.col].k;fd=[...fd].sort((a,b)=>{let va=a[ck],vb=b[ck];if(typeof va==='number'&&typeof vb==='number')return s.asc?va-vb:vb-va;return s.asc?String(va).localeCompare(String(vb)):String(vb).localeCompare(String(va))})}
  let h='<div class="tw"><div class="ttl"><div class="sb"><svg width="14" height="14" fill="none" stroke="var(--slate)" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><input type="text" id="'+fi+'" placeholder="Search..." oninput="renderTable(\\''+containerId+'\\')"></div><div class="rc">'+fd.length+' of '+data.length+'</div></div><div style="overflow-x:auto"><table class="s"><thead><tr>';
  cols.forEach((c,i)=>{const sd=s.col===i;const ar=sd?(s.asc?' \u25b2':' \u25bc'):' \u21c5';h+='<th class="'+(sd?'sd':'')+'" onclick="sortColumn(\\''+containerId+'\\','+i+')">'+c.l+'<span class="si">'+ar+'</span></th>'});
  h+='</tr></thead><tbody>';fd.forEach(r=>{h+='<tr>';cols.forEach(c=>{let v=r[c.k];if(c.fm)v=c.fm(v,r);else if(['mo','ann','rate','hrs','devHrs','testHrs','docHrs','pmHrs','totalHrs','totalCost'].includes(c.k)&&v!=null&&v!=='')v=fmtNum(typeof v==='number'?v:0);if(c.tg)v='<span class="tg '+c.tg(v)+'">'+v+'</span>';h+='<td>'+(v!=null?v:'')+'</td>'});h+='</tr>'});h+='</tbody></table></div></div>';w.innerHTML=h}
function sortColumn(containerId,colIdx){const k=containerId;if(!sortState[k])sortState[k]={col:-1,asc:true};if(sortState[k].col===colIdx)sortState[k].asc=!sortState[k].asc;else{sortState[k].col=colIdx;sortState[k].asc=true}const fe=document.getElementById('f-'+containerId);if(fe)fe.dispatchEvent(new Event('input'))}
""")
print("  [4/8] src/js/tables.js")

# ═══════════════════════════════════════════════
# src/js/calculator.js
# ═══════════════════════════════════════════════
open(f"{P}/src/js/calculator.js","w").write("""let calcState={industry:'',size:'',users:0,branches:0,modules:[],customizations:[],integrations:[],migration:'none',migrationVol:0,training:'basic',support:'email',discount:0};
function toggleChip(el,arr,val){el.classList.toggle('sel');const idx=calcState[arr].indexOf(val);if(idx>=0)calcState[arr].splice(idx,1);else calcState[arr].push(val);recalculate()}
function recalculate(){const s=calcState;let hours=0,bd=[];const dh=s.modules.length>5?24:s.modules.length>2?16:8;hours+=dh;bd.push({c:"Discovery & Requirements",h:dh,cost:dh*BLENDED_RATE});const heavy=['Accounting','Manufacturing','Payroll','E-Commerce','Inventory'];s.modules.forEach(m=>{const cx=s.users>100?'Complex':s.users>30?'Medium':'Simple';const bh=cx==='Simple'?8:cx==='Medium'?16:32;const ml=heavy.includes(m)?1.5:1;const fh=Math.round(bh*ml);hours+=fh;bd.push({c:m+' Configuration',h:fh,cost:fh*BLENDED_RATE})});if(s.branches>1){const bh2=(s.branches-1)*4*s.modules.length;hours+=bh2;bd.push({c:"Multi-Branch Setup",h:bh2,cost:bh2*BLENDED_RATE})}s.customizations.forEach(feat=>{const dv=devCatalog.find(d=>d.feat===feat);if(dv){const t=dv.devHrs+dv.testHrs+dv.docHrs+dv.pmHrs;hours+=t;const dr=dv.devLvl==='AI Engineer'?850:dv.devLvl==='Senior Developer'?650:dv.devLvl==='Data Engineer'?700:500;bd.push({c:'Custom: '+feat,h:t,cost:dv.devHrs*dr+dv.testHrs*450+dv.docHrs*425+dv.pmHrs*650})}});const im={"Portal API (Bayut/Property Finder)":24,"WhatsApp Business API":32,"Payment Gateway":12,"Power BI Connector":20,"REST API":32,"GPS Integration":40,"Biometric Integration":40,"IoT Integration":80,"Document OCR":80,"Mobile App":160};s.integrations.forEach(i2=>{const ih=im[i2]||24;hours+=ih;bd.push({c:'Integration: '+i2,h:ih,cost:ih*BLENDED_RATE})});if(s.migration!=='none'){let mh=s.migration==='simple'?12:s.migration==='medium'?30:60;mh=Math.max(mh,Math.round(s.migrationVol/500));hours+=mh;bd.push({c:"Data Migration",h:mh,cost:mh*BLENDED_RATE})}const th2=s.training==='basic'?8:s.training==='intermediate'?16:32;hours+=th2;bd.push({c:"Training",h:th2,cost:th2*BLENDED_RATE});const gl=s.modules.length>5?16:8;hours+=gl;bd.push({c:"Go-Live Support",h:gl,cost:gl*BLENDED_RATE});const bi=hours*BLENDED_RATE,pm=Math.round(bi*.15),qa=Math.round(bi*.08),doc=Math.round(bi*.05),tst=Math.round(bi*.1),trn=Math.round(bi*.06),cnt=Math.round(bi*.1),gt=bi+pm+qa+doc+tst+trn+cnt,da=Math.round(gt*s.discount/100),fp=gt-da;const sm=s.support==='email'?800:s.support==='priority'?2000:4500,hm=s.users<=20?2800:s.users<=50?4200:5600,wk=Math.max(4,Math.ceil(hours/40));let rt2='Foundation';if(s.customizations.length>0||s.integrations.length>2||s.users>30)rt2='Growth';if(s.customizations.length>2||s.integrations.length>4||s.users>100||s.branches>3)rt2='Enterprise';let tm=['Consultant'];if(hours>80)tm.push('Senior Consultant');if(hours>160)tm.push('Project Manager');if(s.customizations.length>0||s.integrations.length>0)tm.push('Developer');const el=document.getElementById('calc-results');if(!el)return;el.innerHTML='<div class="rp"><h3>Commercial Summary</h3>'+bd.map(b=>'<div class="rr"><span class="rl">'+b.c+'</span><span class="rv">'+fmtAED(b.cost)+' <span style="color:rgba(255,255,255,.35);font-size:12px">('+b.h+'h)</span></span></div>').join('')+'<div style="border-top:1px solid rgba(255,255,255,.1);margin-top:8px;padding-top:8px"><div class="rr"><span class="rl">Base Implementation</span><span class="rv">'+fmtAED(bi)+'</span></div><div class="rr"><span class="rl">Project Management (15%)</span><span class="rv">'+fmtAED(pm)+'</span></div><div class="rr"><span class="rl">Quality Assurance (8%)</span><span class="rv">'+fmtAED(qa)+'</span></div><div class="rr"><span class="rl">Documentation (5%)</span><span class="rv">'+fmtAED(doc)+'</span></div><div class="rr"><span class="rl">Testing (10%)</span><span class="rv">'+fmtAED(tst)+'</span></div><div class="rr"><span class="rl">Training (6%)</span><span class="rv">'+fmtAED(trn)+'</span></div><div class="rr"><span class="rl">Contingency (10%)</span><span class="rv">'+fmtAED(cnt)+'</span></div></div>'+(s.discount>0?'<div class="rr"><span class="rl" style="color:var(--wine)">Discount ('+s.discount+'%)</span><span class="rv" style="color:var(--wine)">-'+fmtAED(da)+'</span></div>':'')+'<div class="rr gr"><span class="rl">FINAL PROPOSAL</span><span class="rv">'+fmtAED(fp)+'</span></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,.1)"><div><div style="font-size:10px;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:1px">Total Hours</div><div style="font-size:22px;font-weight:700;color:var(--gold);margin-top:4px">'+fmtNum(hours)+'</div></div><div><div style="font-size:10px;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:1px">Duration</div><div style="font-size:22px;font-weight:700;color:var(--gold);margin-top:4px">'+wk+' weeks</div></div><div><div style="font-size:10px;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:1px">Monthly Run</div><div style="font-size:22px;font-weight:700;color:var(--gold);margin-top:4px">'+fmtAED(hm+sm)+'</div></div><div><div style="font-size:10px;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:1px">Recommended</div><div style="font-size:22px;font-weight:700;color:var(--gold);margin-top:4px">'+rt2+'</div></div></div><div style="margin-top:12px;font-size:12px;color:rgba(255,255,255,.4)">Team: '+tm.join(' \u00b7 ')+' | Hosting: '+fmtAED(hm)+'/mo | Support: '+fmtAED(sm)+'/mo</div></div>';window._lastCalc={h:hours,bd,bi,pm,qa,doc,tst,trn,cnt,gt,da,fp,sm,hm,wk,rt:rt2,tm,...s}}
function loadIndustryToCalc(name){goToSection('calculator');const ind=industries.find(i=>i.name===name);if(!ind)return;calcState.industry=name;calcState.modules=[...ind.mods];calcState.customizations=[];calcState.integrations=[...ind.ints];setTimeout(()=>{document.getElementById('c-ind').value=name;document.querySelectorAll('#c-mod .mc').forEach(el=>{ind.mods.includes(el.dataset.m)?el.classList.add('sel'):el.classList.remove('sel')});document.querySelectorAll('#c-int .mc').forEach(el=>{ind.ints.includes(el.dataset.m)?el.classList.add('sel'):el.classList.remove('sel')});recalculate();showToast('Loaded '+name+' template')},100)}
""")
print("  [5/8] src/js/calculator.js")

# ═══════════════════════════════════════════════
# src/js/proposal.js + src/js/export.js + src/js/app.js + src/index.html
# ═══════════════════════════════════════════════
# These use the working JS from the previous build, split at function boundaries.

if os.path.exists("sgc-tech-ai-cpq/dist/index.html"):
    src_js = open("sgc-tech-ai-cpq/dist/index.html").read()
    js_content = re.search(r'<script>(.*?)</script>', src_js, re.DOTALL).group(1)

    # Split the JS into proposal, export, and app sections
    # Find function boundaries
    proposal_start = js_content.find("function generateProposal()")
    export_start = js_content.find("function exportFullWorkbook()")
    app_start = js_content.find("const PAGE_TITLES")
    
    if proposal_start and export_start and app_start:
        # proposal.js: generateProposal + loadIndustryToCalc (called from calculator, so put there too)
        open(f"{P}/src/js/proposal.js","w").write(
            "function loadIndustryToCalc(name){goToSection('calculator');const ind=industries.find(i=>i.name===name);if(!ind)return;calcState.industry=name;calcState.modules=[...ind.mods];calcState.customizations=[];calcState.integrations=[...ind.ints];setTimeout(()=>{document.getElementById('c-ind').value=name;document.querySelectorAll('#c-mod .mc').forEach(el=>{ind.mods.includes(el.dataset.m)?el.classList.add('sel'):el.classList.remove('sel')});document.querySelectorAll('#c-int .mc').forEach(el=>{ind.ints.includes(el.dataset.m)?el.classList.add('sel'):el.classList.remove('sel')});recalculate();showToast('Loaded '+name+' template')},100)}\n" +
            js_content[proposal_start:export_start]
        )
        
        # export.js: all export functions
        open(f"{P}/src/js/export.js","w").write(js_content[export_start:app_start])
        
        # app.js: PAGE_TITLES + all render functions + init
        open(f"{P}/src/js/app.js","w").write("const PAGE_TITLES={dashboard:'Dashboard',products:'Master Product Catalog',services:'Implementation Service Catalog',development:'Custom Development Catalog',aisolutions:'AI Solutions Catalog',tiers:'Implementation Tier Matrix',pricing:'Commercial Pricing Matrix',ratecard:'Service Rate Card',rules:'Commercial Rules',industries:'Industry Templates',calculator:'Implementation Calculator',proposal:'Proposal Generator',export:'Export Center'};\nconst tagLic=v=>v==='Subscription'?'tg-n':v==='One-time'?'tg-g':'tg-a';\nconst tagCpx=v=>v==='Simple'?'tg-e':v==='Medium'?'tg-a':'tg-w';\nconst tagDiff=v=>v==='Simple'?'tg-e':v==='Medium'?'tg-a':v==='Complex'?'tg-w':'tg-n';\nconst tagTier=v=>v==='Basic Assistant'?'tg-e':v==='Chatbot'?'tg-a':v==='AI Automation'?'tg-w':v==='Predictive AI'?'tg-n':'tg-g';\nconst tagLvl=v=>v==='L1'?'tg-e':v==='L2'?'tg-a':'tg-n';\n" + js_content[app_start:])

        shutil.rmtree("sgc-tech-ai-cpq", ignore_errors=True)
    
    print("  [6/8] src/js/proposal.js")
    print("  [7/8] src/js/export.js")
    print("  [8/8] src/js/app.js")
else:
    print("  ERROR: Could not extract from previous build. Run the first script first.")
    import sys; sys.exit(1)

# ═══════════════════════════════════════════════
# src/index.html
# ═══════════════════════════════════════════════
open(f"{P}/src/index.html","w").write("""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SGC TECH AI \u2014 Commercial Intelligence Platform</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<link rel="stylesheet" href="css/brand.css">
<link rel="stylesheet" href="css/components.css">
</head><body>
<div class="watermark-bg"></div>
<button class="mt no-print" onclick="document.getElementById('sidebar').classList.toggle('open')" style="display:none;position:fixed;top:12px;left:12px;z-index:200;width:40px;height:40px;background:var(--navy);border:none;border-radius:8px;align-items:center;justify-content:center;cursor:pointer"><svg width="20" height="20" fill="none" stroke="#B79554" stroke-width="2"><path d="M3 6h14M3 10h14M3 14h14"/></svg></button>
<aside id="sidebar"><div class="logo-area"><div class="logo-text">SGC TECH AI</div><div class="logo-sub">Commercial Intelligence</div></div><nav>
<div class="nav-group"><div class="nav-label">Overview</div><div class="nav-item active" data-sec="dashboard"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Dashboard</div></div>
<div class="nav-group"><div class="nav-label">Catalogs</div>
<div class="nav-item" data-sec="products"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>Product Catalog</div>
<div class="nav-item" data-sec="services"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 6V4m0 16v-2M6 12H4m16 0h-2m-1.5-5.5l-1.4 1.4M7.9 16.1l-1.4 1.4m0-11.4l1.4 1.4m8.2 8.2l1.4 1.4"/><circle cx="12" cy="12" r="4"/></svg>Implementation Services</div>
<div class="nav-item" data-sec="development"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>Custom Development</div>
<div class="nav-item" data-sec="aisolutions"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2a4 4 0 014 4c0 1.95-1.4 3.58-3.25 3.93L12 22l-.75-12.07A4.001 4.001 0 0112 2z"/></svg>AI Solutions</div></div>
<div class="nav-group"><div class="nav-label">Commercial</div>
<div class="nav-item" data-sec="tiers"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 6h16M4 12h10M4 18h14"/></svg>Tier Matrix</div>
<div class="nav-item" data-sec="pricing"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Pricing Matrix</div>
<div class="nav-item" data-sec="ratecard"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M2 20h20M5 20V8l7-5 7 5v12M9 20v-6h6v6"/></svg>Rate Card</div>
<div class="nav-item" data-sec="rules"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>Commercial Rules</div></div>
<div class="nav-group"><div class="nav-label">Intelligence</div>
<div class="nav-item" data-sec="industries"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>Industry Templates</div>
<div class="nav-item" data-sec="calculator"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="10" y2="18"/><line x1="14" y1="18" x2="16" y2="18"/></svg>Calculator</div>
<div class="nav-item" data-sec="proposal"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>Proposal Generator</div></div>
<div class="nav-group"><div class="nav-label">Output</div>
<div class="nav-item" data-sec="export"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>Export Center</div></div></nav>
<div class="sidebar-footer"><div class="coord">25.2048 N &nbsp; 55.2708 E</div><div style="font-size:9px;color:rgba(255,255,255,.2);margin-top:4px">v3.0 \u00b7 DIFC, Dubai, UAE</div></div></aside>
<div id="main"><div class="topbar no-print"><h1 id="pt" class="serif">Dashboard</h1><div class="actions"><button class="btn btn-o btn-s" onclick="exportFullWorkbook()"><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>Export Excel</button><button class="btn btn-g btn-s" onclick="goToSection('calculator')"><svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>New Quote</button></div></div>
<section id="sec-dashboard" class="section active"><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-bottom:32px"><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Products</div><div class="kpi-value" id="kp">0</div><div class="kpi-change" style="color:var(--emerald)">Master Catalog</div></div><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Services</div><div class="kpi-value" id="ks">0</div><div class="kpi-change" style="color:var(--emerald)">Implementation</div></div><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Dev Items</div><div class="kpi-value" id="kd">0</div><div class="kpi-change" style="color:var(--emerald)">Custom Dev</div></div><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Industries</div><div class="kpi-value">11</div><div class="kpi-change" style="color:var(--emerald)">Templates</div></div><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Base Rate</div><div class="kpi-value">425</div><div class="kpi-change" style="color:var(--gold)">AED / hour</div></div><div class="kpi-card"><div class="kpi-gold"></div><div class="kpi-label">Rate Roles</div><div class="kpi-value" id="kr">0</div><div class="kpi-change" style="color:var(--emerald)">Rate Card</div></div></div><div style="display:grid;grid-template-columns:2fr 1fr;gap:24px"><div class="cc"><h3>Platform Status</h3><div style="display:flex;align-items:center;gap:8px;margin-bottom:16px"><div class="live-dot"></div><span style="font-size:13px;color:var(--emerald);font-weight:600">System Operational</span></div><div style="font-size:13px;color:var(--slate);line-height:1.8"><div>All commercial catalogs loaded and synchronized.</div><div>Pricing engine active \u2014 AED 425/hr blended rate applied.</div><div>Commercial rules enforced: hours never reduced by discount.</div><div>Excel export engine ready \u2014 10-sheet workbook generation.</div><div>Proposal generator active \u2014 auto-assembly from calculator output.</div></div></div><div class="cc"><h3>Quick Actions</h3><div style="display:flex;flex-direction:column;gap:8px"><button class="btn btn-n" style="justify-content:center;width:100%" onclick="goToSection('calculator')">Implementation Calculator</button><button class="btn btn-g" style="justify-content:center;width:100%" onclick="goToSection('proposal')">Generate Proposal</button><button class="btn btn-o" style="justify-content:center;width:100%" onclick="exportFullWorkbook()">Export Full Workbook</button><button class="btn btn-o" style="justify-content:center;width:100%" onclick="goToSection('products')">Browse Product Catalog</button><button class="btn btn-o" style="justify-content:center;width:100%" onclick="goToSection('industries')">Industry Templates</button></div></div></div></section>
<section id="sec-products" class="section"><div id="tp"></div></section>
<section id="sec-services" class="section"><div id="ts"></div></section>
<section id="sec-development" class="section"><div id="td"></div></section>
<section id="sec-aisolutions" class="section"><div id="ta"></div></section>
<section id="sec-tiers" class="section"><div id="tt"></div></section>
<section id="sec-pricing" class="section"><div id="tpr"></div></section>
<section id="sec-ratecard" class="section"><div id="trc"></div></section>
<section id="sec-rules" class="section"><div id="tru"></div></section>
<section id="sec-industries" class="section"><div id="tin"></div></section>
<section id="sec-calculator" class="section"><div id="tca"></div></section>
<section id="sec-proposal" class="section"><div id="tpr2"></div></section>
<section id="sec-export" class="section"><div id="tex"></div></section>
</div>
<div id="toast" class="toast"><div class="tg2"></div><span id="tmsg"></span></div>
<script src="data/catalogs.js"></script>
<script src="js/utils.js"></script>
<script src="js/tables.js"></script>
<script src="js/calculator.js"></script>
<script src="js/proposal.js"></script>
<script src="js/export.js"></script>
<script src="js/app.js"></script>
</body></html>""")
    print("  [9/11] src/index.html")

# ═══════════════════════════════════════════════
# Build script, README, LICENSE, .gitignore
# ═══════════════════════════════════════════════
open(f"{P}/build.sh","w").write("#!/bin/bash\nset -e\nmkdir -p dist\ncp src/index.html dist/\ncp -r src/css dist/\ncp -r src/js dist/\ncp -r src/data dist/\necho 'Done. Open dist/index.html in your browser.'\n")
os.chmod(f"{P}/build.sh", 0o755)

open(f"{P}/README.md","w").write("""# SGC TECH AI \u2014 Commercial Intelligence Platform\n\n**Source Code Release** \u00b7 v3.0 \u00b7 DIFC, Dubai, UAE\n\n## Quick Start\n\n```bash\n./build.sh && open dist/index.html\n```\n\n## Structure\n```\nsrc/\n\u251c\u2500\u2500 index.html          HTML shell\n\u251c\u2500\u2500 css/\n\u2502\u2514\u2500 brand.css       Design system v3.0\n\u2502\u2514\u2500 components.css  UI components\n\u251c\u2500\u2500 js/\n\u2502\u2514\u2500 utils.js        fmtNum(), fmtAED(), showToast()\n\u2502\u2514\u2500 tables.js       renderTable() with sort/filter\n\u2502\u2514\u2500 calculator.js   Pricing engine (Rule 2 enforced)\n\u2502\u2514\u2500 proposal.js     Proposal generator (Rules 7-10)\n\u2502\u2514\u2500 export.js       Excel export engine\n\u2502\u2514\u2500 app.js          Init + render functions\n\u2514\u2514\u2500 data/\n\u2502   \u2514\u2514\u2500 catalogs.js     10 data arrays\n\u2502\u2514\u2500 dist/                   Built output\n```\n\n## Pricing\n- Base Rate: **AED 425/hour** blended\n- Overhead: 1.54x (54%)\n- Discount: Never reduces hours (Rule 2)\n""")

open(f"{P}/LICENSE","w").write("PROPRIETARY AND CONFIDENTIAL\n\nCopyright (c) 2025 Scholarix Global Consultants FZE (SGC TECH AI)\nDIFC, Dubai, United Arab Emirates\n\nAll rights reserved.\n")

open(f"{P}/.gitignore","w").write("node_modules/\n.DS_Store\n*.tar.gz\ndist/\n")

# ═══════════════════════════════════════════════
# Build dist/ and create tar
# ═══════════════════════════════════════════════
os.chdir(f"/home/sgctechai")
subprocess.run(["bash","build.sh"], cwd=P, check=True)

import tarfile
with tarfile.open("sgc-tech-ai-cpq-src.tar.gz", "w:gz") as tar:
    tar.add(P, arcname="sgc-tech-ai-cpq-src")

# Count files
file_count = sum(len(files) for _, _, files in os.walk(P))
total_size = sum(os.path.get(os.path.join(r,f),0) for r,d,files in os.walk(P))

print()
print("\u2550" * 60)
print("  SGC TECH AI \u2014 Source Code Scaffold")
print("\u2550" * 60)
print(f"\n  File:   sgc-tech-ai-cpq-src.tar.gz")
print(f"  Size:   {os.path.getsize('sgc-tech-ai-cpq-src.tar.gz') / 1024}KB")
print(f"  Files:  {file_count} across 8 directories")
print()
print("  src/")
for r, d, files in os.walk(f"{P}/src"):
    level = r.replace(P, "").count(os.sep)
    indent = "  " * (level + 1)
    print(f"{indent}{d}/")
    for f in sorted(files):
        size = os.path.get(os.path.join(r, f), 0)
        print(f"{indent}  {f}  ({size:,} bytes)")
print()
print("  To edit:  cd sgc-tech-ai-cpq-src && code .")
print("  To run:  ./build.sh && open dist/index.html")
print()
print("\u2550" * 60)