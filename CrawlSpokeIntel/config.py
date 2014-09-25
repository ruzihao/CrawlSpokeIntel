DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '976269',
    'database': 'companies'
}

TABLES = {
    'table_companies_name': 'si_companies',
    'table_members_name': 'si_members',
    'table_fundings_name': 'si_fundings',
    'table_acquisitions_name': 'si_acquisitions',
    'table_investors_name': 'si_investors'
}

TABLE_COMPANIES_COLS = {
    'name': 'name',
    'short_des': 'short_description',
    'website': 'website',
    'blog': 'blog',
    'summary': 'summary',
    'status': 'status',
    'founded_on': 'founded_on',
    'year_rev': 'yearly_revenue',
    'industry': 'industry',
    'people': 'people',
    'alias': 'alias',
    'tags': 'tags',
    'location': 'location',
    'tel': 'contact_info_tel',
    'email': 'contact_info_email',
    'branch': 'branch',
    'addr': 'address_line',
    'city': 'city',
    'state': 'state',
    'ps_code': 'postal_code',
    'country': 'country'
}

TABLE_MEMBERS_COLS = {
    'name': 'name',
    'title': 'title',
    'cat': 'category',
    'since': 'since',
    'members': 'members'
}

TABLE_FUNDINGS_COLS = {
    'date': 'date',
    'series': 'series',
    'amount': 'amount',
    'investors': 'investors'
}

TABLE_ACQUISITIONS_COLS = {
    'name': 'name',
    'since': 'since',
    'status': 'status'
}

TABLE_INVESTORS_COLS = {
    'name': 'name',
    'since': 'since',
    'series': 'series'
}
