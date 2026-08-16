"""Seed URLs for the ZAIO website crawl (Capstone Day 1 scope).

Why a fixed seed list?
A bounded crawl is reliable for marking: we cover courses, FAQs, financing,
and about pages without chasing login or external apps.
"""

SEED_URLS: list[str] = [
    "https://www.zaio.io/",
    "https://www.zaio.io/bootcamps",
    "https://www.zaio.io/compare-courses",
    "https://www.zaio.io/tuition-financing",
    "https://www.zaio.io/aboutus",
    "https://www.zaio.io/qualifications",
    "https://www.zaio.io/fullstack-ai-engineer-bootcamp",
    "https://www.zaio.io/fullstack-bootcamp",
    "https://www.zaio.io/datascience-bootcamp",
    "https://www.zaio.io/cybersecurity-bootcamp",
    "https://www.zaio.io/digital-marketing-bootcamp",
    "https://www.zaio.io/company",
    "https://www.zaio.io/learner-stories",
    "https://www.zaio.io/events",
    "https://www.zaio.io/terms",
]

# These routes returned an empty JS shell with httpx (no server-rendered text):
# /community, /cloud-devops-engineer-bootcamp, /refundPolicy
# Cloud/DevOps is still covered via /bootcamps and /compare-courses.

# Hosts / path prefixes we will not crawl.
SKIP_PREFIXES: tuple[str, ...] = (
    "https://www.zaio.io/app/login",
    "https://applications.zaio.io/",
    "mailto:",
    "https://www.trustpilot.com/",
)
