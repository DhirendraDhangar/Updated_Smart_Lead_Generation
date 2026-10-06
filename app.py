from src.input_handler import get_user_input
from src.lead_search_engine import search_leads
from src.deduplication import remove_duplicates
from src.export_service import export_csv
from src.website_analyzer import analyze_websites
def main():
    print('LEAD GENERATION SYSTEM')
    print('_______________\n')
    location,industry,num_leads=get_user_input()
    print('Searching...')
    print(f'Industry: {industry}')
    print(f'Location: {location}\n')
    leads=search_leads(location,industry,num_leads)
    unique,dup,dup_count,new_count=remove_duplicates(leads)
    print("\nAnalyzing Websites....\n")
    unique = analyze_websites(unique)

    total=export_csv(unique)
    print(f'Results generated: {len(leads)}\n')
    if dup_count:
        print(f'Duplicates found: {dup_count} leads are already present in the database.\n')
    print('===================================')
    print('       SEARCH COMPLETED')
    print('===================================\n')
    print(f'New Leads Added: {new_count}')
    print(f'Total Leads in Database: {total}\n')
    print('Data saved in:')
    print('data/all_leads_database.csv')
if __name__=='__main__':
    main()
