# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb as msd
import config as cf

from items import CrawlspokeintelItem


DB = cf.DATABASE
TABLES = cf.TABLES
TC = cf.TABLE_COMPANIES_COLS
# HOST = 'localhost'
# USER = 'root'
# PASSWD = '976269'
# DATABASE = 'companies'

# TABLE_COMPANY = 'si_companies'
# TABLE_MEMBERS = 'si_members'
# TABLE_FUNDINGS = 'si_fundings'
# TABLE_ACQUISITION = 'si_acquisitions'
# TABLE_INVESTORS = 'si_investors'


class CrawlspokeintelPipeline(object):
    def __init__(self):
        self.conn = msd.connect(host=DB['host'], user=DB['user'], passwd=DB['passwd'], db=DB['database'])
        self.cur = self.conn.cursor()
        self._create_tables(self.cur, TABLES)


    def _create_tables(self, cur=None, tables=None):
        ct_dict = self._create_tables_str(tables)
        for k, v in ct_dict.iteritems():
            cur.execute(self._gen_drop_table_str(k))
            cur.execute(self._gen_create_table_str(k, v.keys(), v.values()))
        return


    def _create_tables_str(self, tables=None):
        tables_dict = {}
        excluded_keys = ('members',
                         'funding_history',
                         'funding_investors',
                         'investments')
        # create table si_companies
        col_names = [k for k in TC.values() if k not in excluded_keys]
        col_types_dict = dict.fromkeys(col_names, 'text')
        tables_dict[tables['table_companies_name']] = col_types_dict

        # map other 4 tables to their column names
        tables_dict[tables['table_members_name']] = dict.fromkeys(cf.TABLE_MEMBERS_COLS.values(), 'text')
        tables_dict[tables['table_fundings_name']] = dict.fromkeys(cf.TABLE_FUNDINGS_COLS.values(), 'text')
        tables_dict[tables['table_acquisitions_name']] = dict.fromkeys(cf.TABLE_ACQUISITIONS_COLS.values(), 'text')
        tables_dict[tables['table_investors_name']] = dict.fromkeys(cf.TABLE_INVESTORS_COLS.values(), 'text')

        return tables_dict


    def _gen_drop_table_str(self, table_name):
        ''' Generalized string generator for table dropping. '''
        return 'drop table if exists %s;'%table_name


    def _gen_create_table_str(self, table_name, col_names, col_types):
        ''' Generalized string generator for table creating. '''
        assert len(col_names) == len(col_types)
        name_type_str = ', '.join([' '.join(row) for row in zip(col_names, col_types)])
        new_str = 'create table %(tname)s (%(nstr)s);'%{'tname': table_name, 'nstr': name_type_str}
        return new_str

    def process_item(self, item, spider):
        return item


def main():
    ''' For testing. '''
    obj = CrawlspokeintelPipeline()
    # print obj._gen_create_table_str(TABLES['table_companies_name'], ('name', 'price'), ('text', 'text'))
    # print obj._gen_drop_table_str(TABLES['table_companies_name'])


if __name__ == '__main__':
    main()