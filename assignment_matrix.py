ASSIGNMENT_MATRIX = [
    {"Region": "Global", "BU": "ACL(CLS/PTS)", "SiteLeaders": ["Jeremy Zeiders"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ACL(IND)", "SiteLeaders": ["Jeff Qian"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ADM", "SiteLeaders": ["Alison Combs"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ENG", "SiteLeaders": ["Iwona Cristea", "Karolina Wawrzyk"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "DDN", "SiteLeaders": ["Monica Zhu"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "MED", "SiteLeaders": ["Derek Wu"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ASG", "SiteLeaders": ["Spandana Dittakavi"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "AMER", "BU": "AUT-AMER", "SiteLeaders": ["Juan Luis Martin"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "EMEA", "BU": "AUT-EMIA", "SiteLeaders": ["Martin Adamek"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "AP", "BU": "AUT-AP", "SiteLeaders": ["Polly Pang"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ICT", "SiteLeaders": ["Samantha Matte"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "SEN", "SiteLeaders": ["Raymond Keenan"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "ELECs", "SiteLeaders": ["Cyril Suel"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "INDIRECT", "SiteLeaders": ["Christie Han"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "METALs", "SiteLeaders": ["Brandon Hess"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]},
    {"Region": "Global", "BU": "RESINs", "SiteLeaders": ["Denisse Benitez"], "ContactEmail": ["rose.fuentes@te.com"], "TEOALeaders": ["Alexis Rydbom", "Cassie Cong"], "TEOAEmails": ["rose.fuentes@te.com"]}
]

def normalize_region(region):
    """Normalize region - handle case-insensitive and NA/AMER fallback"""
    if not region:
        return ""
    region = region.strip()
    region_lower = region.lower()
    if region_lower == "na" or region_lower == "amer":
        return "AMER"
    return region

def get_assignment(region, bu):
    """
    Get site leader and TEOA leader based on Region and BU.
    Returns dict with site_leaders, teoa_leaders, emails, site_leader_str, teoa_leader_str
    Uses case-insensitive matching with NA/AMER fallback
    """
    if not region or not bu:
        return {
            "site_leaders": [],
            "teoa_leaders": [],
            "emails": [],
            "site_leader_str": "",
            "teoa_leader_str": ""
        }
    
    normalized_region = normalize_region(region)
    bu_norm = bu.strip()
    
    for entry in ASSIGNMENT_MATRIX:
        entry_region = entry["Region"].strip()
        entry_bu = entry["BU"].strip()
        
        if entry_region == normalized_region and entry_bu == bu_norm:
            return {
                "site_leaders": entry["SiteLeaders"],
                "teoa_leaders": entry["TEOALeaders"],
                "emails": entry["TEOAEmails"] + entry["ContactEmail"],
                "site_leader_str": ", ".join(entry["SiteLeaders"]),
                "teoa_leader_str": ", ".join(entry["TEOALeaders"])
            }
    
    return {
        "site_leaders": [],
        "teoa_leaders": [],
        "emails": [],
        "site_leader_str": "No mapping found",
        "teoa_leader_str": "No mapping found"
    }

def get_all_regions():
    """Get unique regions from the matrix"""
    regions = set()
    for entry in ASSIGNMENT_MATRIX:
        regions.add(entry["Region"])
    return sorted(list(regions))

def get_bus_by_region(region):
    """Get BUs for a specific region"""
    bus = []
    for entry in ASSIGNMENT_MATRIX:
        if entry["Region"] == region:
            bus.append(entry["BU"])
    return bus
