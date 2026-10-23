"""HabariMCP — Kenya Civic Information Tools (5 tools). All data DEMO."""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

# Annotations tell clients which tools are safe to auto-approve (read-only, no side effects).
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": False}

try:
    _VERSION = _pkg_version("habari-mcp")
except PackageNotFoundError:  # a source tree that was never installed
    _VERSION = "0+unknown"


mcp = FastMCP(name="habari-mcp", instructions="Kenya civic information: gazette, tenders, open data. DEMO.", version=_VERSION)

@mcp.tool(name="gazette_search", description="Explain the types of notice in the Kenya Gazette (legal notices, appointments, company notices and others) and where to read the Gazette. Use when someone asks what a Gazette notice type is or how to find one. search_type matches a type by name; an unrecognised type returns an error listing the valid ones. date_range is only echoed back. This tool does NOT search the Gazette. Returns the type description and the access points (kenyalaw.org). Labelled DEMO. Read-only; no side effects.", annotations=READ_ONLY)
def gazette_search(search_type: Annotated[str, Field(description="Notice type such as legal_notice, appointment or company_notice; an unrecognised type returns an error.")], date_range: Annotated[str | None, Field(description="Optional; only echoed back.")] = None) -> dict:
    TYPES = {
        "legal_notice": "Statutory rules, regulations, and subsidiary legislation. Numbered sequentially each year.",
        "appointment": "Government officer appointments, board memberships, parastatal officials.",
        "company_notice": "Company dissolutions, name changes, insolvency notices.",
        "land_notice": "Compulsory acquisition, boundaries, adjudication notices.",
        "tender_notice": "Some government tenders gazetted here. See tender_search for IFMIS tenders.",
    }
    t = search_type.lower()
    desc = next((v for k, v in TYPES.items() if k in t), None)
    if desc is None:
        return {"error": f"Unknown notice type {search_type!r}.", "valid_types": list(TYPES)}
    return {"source": "DEMO — kenyalaw.org for official Kenya Gazette", "search_type": search_type,
            "description": desc, "access": "kenyalaw.org/kenya_gazette — free online. Kenya National Library for physical copies.",
            "api": "Kenya Gazette API: api.kenyalaw.org (if available)", "date_range": date_range}

@mcp.tool(name="tender_search_guide", description="Where to find Kenyan public tenders and what bidders need: the IFMIS eTender portal, county eProcurement, the Gazette, eligibility documents and tender value thresholds. Use when someone asks how to find or qualify for a tender. sector and county are only echoed back; this tool does NOT list live tenders. Returns the portals, eligibility requirements and thresholds. Labelled DEMO: confirm at tenders.go.ke. Read-only; no side effects.", annotations=READ_ONLY)
def tender_search_guide(sector: Annotated[str | None, Field(description="Optional sector; only echoed back.")] = None, county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None) -> dict:
    return {"source": "DEMO — tenders.go.ke for official tenders", "sector": sector, "county": county,
            "portals": [
                {"name": "IFMIS eTender Portal", "url": "tenders.go.ke", "coverage": "All national government tenders"},
                {"name": "County eProcurement", "url": "varies by county", "coverage": "County-level procurement"},
                {"name": "PPRA Public Portal", "url": "ppra.go.ke", "coverage": "Regulatory oversight + debarred firms"},
                {"name": "Gazette Supplement", "url": "kenyalaw.org", "coverage": "Gazetted tender notices"},
            ],
            "eligibility": "Tax Compliance Certificate (KRA), Business Registration, Audited Accounts required for most tenders.",
            "thresholds": {"open_tender": "Above KES 30M (national), KES 10M (county)",
                           "restricted": "KES 3M–30M", "quotation": "Under KES 3M"}}

@mcp.tool(name="open_data_guide", description="Where to find Kenyan open data by topic (population, health, budget and others) with the publisher, URL and format. Use when someone asks where to get official data. data_type matches a category by name; if none match, the general Kenya Open Data portal is returned. Returns the matching sources and all_categories. Portal addresses labelled DEMO and subject to change. Read-only; no side effects.", annotations=READ_ONLY)
def open_data_guide(data_type: Annotated[str, Field(description="Data category such as population, health or budget.")]) -> dict:
    SOURCES = {
        "population": {"source": "Kenya National Bureau of Statistics (KNBS)", "url": "knbs.or.ke/open-data", "format": "CSV/API"},
        "health": {"source": "Kenya Health Information System (DHIS2)", "url": "hiskenya.org", "format": "API/CSV"},
        "budget": {"source": "National Treasury Open Data", "url": "opendata.go.ke", "format": "CSV/JSON"},
        "land": {"source": "Lands Ministry / NLC", "url": "lands.go.ke", "format": "Limited open access"},
        "weather": {"source": "Kenya Meteorological Department", "url": "meteo.go.ke", "format": "API/PDF"},
        "elections": {"source": "IEBC Open Data", "url": "iebc.or.ke", "format": "PDF/CSV"},
        "parliament": {"source": "National Assembly Hansard", "url": "parliament.go.ke", "format": "PDF"},
        "company_registry": {"source": "Business Registration Service", "url": "ecitizen.go.ke", "format": "Paid search"},
    }
    dt = data_type.lower()
    matched = {k: v for k, v in SOURCES.items() if k in dt or dt in k}
    return {"source": "DEMO — portals subject to change", "data_type": data_type,
            "sources": matched or {"general": "opendata.go.ke — Kenya Open Data Portal"},
            "all_categories": list(SOURCES.keys())}

@mcp.tool(name="parliament_tracker", description="How to follow the Parliament of Kenya: the bills tracker, Hansard, committees and related. Use when someone asks how to track a bill or find a debate. Keywords in query_type select entries; if none match, ALL guidance is returned. This tool does NOT fetch live bill status. Returns the information and the parliament.go.ke portal. Labelled DEMO. Read-only; no side effects.", annotations=READ_ONLY)
def parliament_tracker(query_type: Annotated[str, Field(description="What to track, such as bill, hansard or committee.")]) -> dict:
    GUIDE = {
        "bill": "Bills tracker: parliament.go.ke → Bills. First reading → Second (debate) → Committee → Third → Senate → Presidential assent.",
        "hansard": "Daily Hansard (verbatim record): parliament.go.ke → Hansard. Searchable by keyword/MP name.",
        "committee": "13 departmental committees. Attend public hearings. Submissions accepted by email to committee clerk.",
        "petition": "Citizens can petition Parliament. Must have 1,000+ signatures. Tabled by MP or direct submission.",
        "mp_contacts": "Find your MP: parliament.go.ke → Members. Email/phone listed. County allocation questions → County Assembly.",
    }
    t = query_type.lower()
    matched = {k: v for k, v in GUIDE.items() if k in t}
    return {"source": "DEMO — parliament.go.ke", "query": query_type,
            "information": matched or GUIDE, "portal": "parliament.go.ke"}

@mcp.tool(name="citizen_feedback_channels", description="Where to report a problem to Kenyan authorities by issue type, such as corruption (EACC) or service delivery, with contact details. Use when someone asks where to complain. Keywords in issue_type select channels; if none match, the eCitizen portal is returned. Returns the channels and all_categories. Contact numbers are labelled DEMO and unverified: confirm before relying. Read-only; no side effects.", annotations=READ_ONLY)
def citizen_feedback_channels(issue_type: Annotated[str, Field(description="Issue such as corruption or service_delivery.")]) -> dict:
    CHANNELS = {
        "corruption": ["Ethics and Anti-Corruption Commission (EACC): eacc.go.ke | 0800722000 (free)",
                       "Kenya Audit Institute: kenao.go.ke", "Director of Public Prosecutions: odpp.go.ke"],
        "service_delivery": ["Kenya Citizens and Foreign Nationals Management Service: 0800722000",
                              "County Ombudsman", "National Assembly Petitions Committee"],
        "human_rights": ["Kenya National Human Rights Commission: knchr.org | 020-2270000",
                         "County Human Rights Committees"],
        "police": ["Independent Policing Oversight Authority (IPOA): ipoa.go.ke | 0800720627",
                   "Internal Affairs Unit (IAU) of NPS"],
        "election": ["IEBC: iebc.or.ke | 0800724242 (election period)", "Election Court petition (within 28 days)"],
    }
    t = issue_type.lower()
    matched = {k: v for k, v in CHANNELS.items() if k in t or any(w in t for w in k.split("_"))}
    return {"source": "DEMO", "issue_type": issue_type,
            "channels": matched or {"general": "eCitizen portal: ecitizen.go.ke"},
            "all_categories": list(CHANNELS.keys())}

def main() -> None:
    """Console entry point."""
    mcp.run()
