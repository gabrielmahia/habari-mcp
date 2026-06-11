"""HabariMCP — Kenya Civic Information Tools (5 tools). All data DEMO."""
from __future__ import annotations
from typing import Optional
from fastmcp import FastMCP
mcp = FastMCP(name="habari-mcp", description="Kenya civic information: gazette, tenders, open data. DEMO.")

@mcp.tool(name="gazette_search", description="Guide to searching Kenya Gazette for legal notices, regulations, and appointments. DEMO.")
def gazette_search(search_type: str, date_range: Optional[str] = None) -> dict:
    TYPES = {
        "legal_notice": "Statutory rules, regulations, and subsidiary legislation. Numbered sequentially each year.",
        "appointment": "Government officer appointments, board memberships, parastatal officials.",
        "company_notice": "Company dissolutions, name changes, insolvency notices.",
        "land_notice": "Compulsory acquisition, boundaries, adjudication notices.",
        "tender_notice": "Some government tenders gazetted here. See tender_search for IFMIS tenders.",
    }
    t = search_type.lower()
    desc = next((v for k, v in TYPES.items() if k in t), TYPES["legal_notice"])
    return {"source": "DEMO — kenyalaw.org for official Kenya Gazette", "search_type": search_type,
            "description": desc, "access": "kenyalaw.org/kenya_gazette — free online. Kenya National Library for physical copies.",
            "api": "Kenya Gazette API: api.kenyalaw.org (if available)", "date_range": date_range}

@mcp.tool(name="tender_search_guide", description="Guide to finding and accessing Kenya government tenders. DEMO.")
def tender_search_guide(sector: Optional[str] = None, county: Optional[str] = None) -> dict:
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

@mcp.tool(name="open_data_guide", description="Kenya open government data sources and APIs. DEMO.")
def open_data_guide(data_type: str) -> dict:
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

@mcp.tool(name="parliament_tracker", description="Track Kenya parliament: bills, Hansard, committees, and petitions. DEMO.")
def parliament_tracker(query_type: str) -> dict:
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

@mcp.tool(name="citizen_feedback_channels", description="Official channels for Kenyan citizen feedback, complaints, and government access. DEMO.")
def citizen_feedback_channels(issue_type: str) -> dict:
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
