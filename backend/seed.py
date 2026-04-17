"""Seed the database with sample HCPs and interactions for demo."""
from database import SessionLocal, engine, Base
from models import HCP, Interaction, FollowUp
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if already seeded
if db.query(HCP).count() > 0:
    print("Database already seeded. Skipping.")
    db.close()
    exit(0)

# ─── Sample HCPs ───
hcps = [
    HCP(name="Dr. Sarah Smith", specialty="Cardiology", organization="Metro Heart Center", email="sarah.smith@metroheart.com", phone="+1-555-0101", territory="Northeast"),
    HCP(name="Dr. James Wilson", specialty="Oncology", organization="City Cancer Institute", email="j.wilson@citycancer.org", phone="+1-555-0102", territory="Southeast"),
    HCP(name="Dr. Emily Chen", specialty="Neurology", organization="Braincare Medical", email="e.chen@braincare.com", phone="+1-555-0103", territory="West"),
    HCP(name="Dr. Michael Brown", specialty="Endocrinology", organization="Diabetes Care Clinic", email="m.brown@diabetescare.com", phone="+1-555-0104", territory="Midwest"),
    HCP(name="Dr. Priya Patel", specialty="Rheumatology", organization="Joint Health Associates", email="p.patel@jointhealth.com", phone="+1-555-0105", territory="South"),
    HCP(name="Dr. Robert Kim", specialty="Pulmonology", organization="Lung & Respiratory Center", email="r.kim@lungcenter.com", phone="+1-555-0106", territory="Northeast"),
    HCP(name="Dr. Lisa Anderson", specialty="Dermatology", organization="Skin Health Clinic", email="l.anderson@skinhealth.com", phone="+1-555-0107", territory="West"),
    HCP(name="Dr. David Martinez", specialty="Gastroenterology", organization="Digestive Health Institute", email="d.martinez@digestivehealth.com", phone="+1-555-0108", territory="South"),
]

for hcp in hcps:
    db.add(hcp)
db.commit()

print(f"Added {len(hcps)} HCPs")

# ─── Sample Interactions ───
today = datetime.now()
interactions = [
    Interaction(
        hcp_id=1, interaction_type="Meeting", date=(today - timedelta(days=2)).strftime("%Y-%m-%d"),
        time="10:00 AM", attendees="Dr. Sarah Smith, John (Sales Rep)",
        topics_discussed="Product X efficacy data, new clinical trial results",
        notes="Dr. Smith was very interested in the Phase 3 trial data for Product X. She mentioned she has several patients who could benefit.",
        summary="Discussed Product X clinical data with Dr. Smith who showed strong interest",
        sentiment="Positive", outcomes="Dr. Smith agreed to review the clinical data package",
        materials_shared="Brochures, Clinical Trial Summary", samples_distributed="Product X samples (3 units)",
        follow_up_actions="Send full clinical data package by email",
    ),
    Interaction(
        hcp_id=2, interaction_type="Call", date=(today - timedelta(days=5)).strftime("%Y-%m-%d"),
        time="02:30 PM", attendees="Dr. James Wilson",
        topics_discussed="Oncology treatment protocol updates, Product Y availability",
        notes="Dr. Wilson expressed concerns about the pricing of Product Y but was interested in the patient assistance program.",
        summary="Discussed Product Y pricing concerns and patient assistance program",
        sentiment="Neutral", outcomes="Will send pricing comparison and patient assistance info",
        materials_shared="Product Y brochure", samples_distributed="",
        follow_up_actions="Schedule in-person meeting next week",
    ),
    Interaction(
        hcp_id=3, interaction_type="Conference", date=(today - timedelta(days=10)).strftime("%Y-%m-%d"),
        time="09:00 AM", attendees="Dr. Emily Chen, Dr. Smith, Multiple attendees",
        topics_discussed="Neurology symposium, latest research in Alzheimer's treatment",
        notes="Met Dr. Chen at the annual neurology symposium. She was presenting research on early-stage Alzheimer's detection.",
        summary="Connected with Dr. Chen at neurology symposium about Alzheimer's research",
        sentiment="Positive", outcomes="Dr. Chen interested in our Alzheimer's pipeline drugs",
        materials_shared="Pipeline overview poster", samples_distributed="",
        follow_up_actions="Arrange a detailed meeting about pipeline drugs",
    ),
    Interaction(
        hcp_id=4, interaction_type="Visit", date=(today - timedelta(days=1)).strftime("%Y-%m-%d"),
        time="11:00 AM", attendees="Dr. Michael Brown, Clinic Staff",
        topics_discussed="Diabetes management tools, Product Z insulin pump",
        notes="Visited Dr. Brown at his clinic. He was hesitant about switching from current insulin pump brand but willing to see a demo.",
        summary="Product Z insulin pump demo discussion with Dr. Brown",
        sentiment="Neutral", outcomes="Demo scheduled for next month",
        materials_shared="Product Z specification sheet", samples_distributed="Product Z demo unit",
        follow_up_actions="Schedule product demo, send comparison chart",
    ),
]

for interaction in interactions:
    db.add(interaction)
db.commit()

print(f"Added {len(interactions)} interactions")

# ─── Sample Follow-ups ───
follow_ups = [
    FollowUp(interaction_id=1, date=(today + timedelta(days=3)).strftime("%Y-%m-%d"), follow_up_type="Email", notes="Send full clinical data package for Product X", status="Pending"),
    FollowUp(interaction_id=2, date=(today + timedelta(days=5)).strftime("%Y-%m-%d"), follow_up_type="Meeting", notes="In-person meeting to discuss Product Y pricing", status="Pending"),
    FollowUp(interaction_id=4, date=(today + timedelta(days=14)).strftime("%Y-%m-%d"), follow_up_type="Visit", notes="Product Z demo at Dr. Brown's clinic", status="Pending"),
]

for fu in follow_ups:
    db.add(fu)
db.commit()

print(f"Added {len(follow_ups)} follow-ups")
print("Database seeded successfully!")
db.close()
