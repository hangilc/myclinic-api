
import requests
url = "http://127.0.0.1:28080/json"

def search_byoumei(text, at):
    params = { 'text': text, 'at': at }
    r = requests.get(url + '/search-byoumei-master', params=params)
    return r.json()


def list_visit_by_patient_having_hoken(patient_id, year, month):
    params = { 'patient-id': patient_id, 'year': year, 'month': month }
    r = requests.get(url + '/list-visit-by-patient-having-hoken', params=params)
    return r.json()


def list_recently_registered_patients(n):
    params = { 'n': n }
    r = requests.get(url + '/list-recently-registered-patients', params=params)
    return r.json()


def list_todays_hotline_in_range(after, before):
    params = { 'after': after, 'before': before }
    r = requests.get(url + '/list-todays-hotline-in-range', params=params)
    return r.json()


def list_todays_visits():
    r = requests.get(url + '/list-todays-visits')
    return r.json()


def batch_get_drug_attr(drug_ids):
    params = { 'drug-ids': drug_ids }
    r = requests.get(url + '/batch-get-drug-attr', params=params)
    return r.json()


def get_drug_full(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.get(url + '/get-drug-full', params=params)
    return r.json()


def get_shinryou_full(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.get(url + '/get-shinryou-full', params=params)
    return r.json()


def convert_to_hoken(visit):
    data = visit
    r = requests.post(url + '/convert-to-hoken', data=data)
    return r.json()


def batch_delete_drugs(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.post(url + '/batch-delete-drugs', params=params)
    return r.json()


def get_conduct_kizai_full(conduct_kizai_id):
    params = { 'conduct-kizai-id': conduct_kizai_id }
    r = requests.get(url + '/get-conduct-kizai-full', params=params)
    return r.json()


def find_byoumei_master_by_name(name, at):
    params = { 'name': name, 'at': at }
    r = requests.get(url + '/find-byoumei-master-by-name', params=params)
    return r.json()


def list_disease_example():
    r = requests.get(url + '/list-disease-example')
    return r.json()


def list_drug_full_by_drug_ids(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.get(url + '/list-drug-full-by-drug-ids', params=params)
    return r.json()


def list_wqueue_full():
    r = requests.get(url + '/list-wqueue-full')
    return r.json()


def get_shahokokuho(shahokokuho_id):
    params = { 'shahokokuho-id': shahokokuho_id }
    r = requests.get(url + '/get-shahokokuho', params=params)
    return r.json()


def batch_resolve_shinryou_names(at, args):
    params = { 'at': at }
    data = args
    r = requests.post(url + '/batch-resolve-shinryou-names', params=params, data=data)
    return r.json()


def delete_conduct_kizai(conduct_kizai_id):
    params = { 'conduct-kizai-id': conduct_kizai_id }
    r = requests.post(url + '/delete-conduct-kizai', params=params)
    return r.json()


def get_pharma_queue_full(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-pharma-queue-full', params=params)
    return r.json()


def enter_shinryou_attr(attr):
    data = attr
    r = requests.post(url + '/enter-shinryou-attr', data=data)
    return r.json()


def delete_gazou_label(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.post(url + '/delete-gazou-label', params=params)
    return r.json()


def find_shinryou_attr(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.get(url + '/find-shinryou-attr', params=params)
    return r.json()


def list_visit_full_2(patient_id, page):
    params = { 'patient-id': patient_id, 'page': page }
    r = requests.get(url + '/list-visit-full2', params=params)
    return r.json()


def get_text(text_id):
    params = { 'text-id': text_id }
    r = requests.get(url + '/get-text', params=params)
    return r.json()


def enter_conduct_full(arg):
    data = arg
    r = requests.post(url + '/enter-conduct-full', data=data)
    return r.json()


def find_shouki(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/find-shouki', params=params)
    return r.json()


def list_conduct_full_by_ids(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.get(url + '/list-conduct-full-by-ids', params=params)
    return r.json()


def get_kouhi(kouhi_id):
    params = { 'kouhi-id': kouhi_id }
    r = requests.get(url + '/get-kouhi', params=params)
    return r.json()


def enter_shouki(shouki):
    data = shouki
    r = requests.post(url + '/enter-shouki', data=data)
    return r.json()


def list_hokensho(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-hokensho', params=params)
    return r.json()


def delete_koukikourei(koukikourei):
    data = koukikourei
    r = requests.post(url + '/delete-koukikourei', data=data)
    return r.json()


def list_disease_full(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-disease-full', params=params)
    return r.json()


def list_hoken(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-hoken', params=params)
    return r.json()


def delete_shouki(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/delete-shouki', params=params)
    return r.json()


def find_drug_attr(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.get(url + '/find-drug-attr', params=params)
    return r.json()


def update_hoken(hoken):
    data = hoken
    r = requests.post(url + '/update-hoken', data=data)
    return r.json()


def list_visit_text_drug_by_patient_and_iyakuhincode(patient_id, iyakuhincode, page):
    params = { 'patient-id': patient_id, 'iyakuhincode': iyakuhincode, 'page': page }
    r = requests.get(url + '/list-visit-text-drug-by-patient-and-iyakuhincode', params=params)
    return r.json()


def get_wqueue_full(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-wqueue-full', params=params)
    return r.json()


def list_shinryou_full(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/list-shinryou-full', params=params)
    return r.json()


def search_shinryou_master(text, at):
    params = { 'text': text, 'at': at }
    r = requests.get(url + '/search-shinryou-master', params=params)
    return r.json()


def batch_enter_shinryou_by_name(name, visit_id):
    params = { 'name': name, 'visit-id': visit_id }
    r = requests.post(url + '/batch-enter-shinryou-by-name', params=params)
    return r.json()


def enter_conduct_kizai(conduct_kizai):
    data = conduct_kizai
    r = requests.post(url + '/enter-conduct-kizai', data=data)
    return r.json()


def batch_enter_drugs(drugs):
    data = drugs
    r = requests.post(url + '/batch-enter-drugs', data=data)
    return r.json()


def delete_disease(disease_id):
    params = { 'disease-id': disease_id }
    r = requests.post(url + '/delete-disease', params=params)
    return r.json()


def batch_resolve_iyakuhin_master(iyakuhincode, at):
    params = { 'iyakuhincode': iyakuhincode, 'at': at }
    r = requests.get(url + '/batch-resolve-iyakuhin-master', params=params)
    return r.json()


def get_clinic_info():
    r = requests.get(url + '/get-clinic-info')
    return r.json()


def list_all_pharma_drug_names():
    r = requests.get(url + '/list-all-pharma-drug-names')
    return r.json()


def list_payment(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/list-payment', params=params)
    return r.json()


def list_visit_id_visited_at_by_patient_and_iyakuhincode(patient_id, iyakuhincode):
    params = { 'patient-id': patient_id, 'iyakuhincode': iyakuhincode }
    r = requests.get(url + '/list-visit-id-visited-at-by-patient-and-iyakuhincode', params=params)
    return r.json()


def batch_delete_shinryou(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.post(url + '/batch-delete-shinryou', params=params)
    return r.json()


def list_current_disease_full(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-current-disease-full', params=params)
    return r.json()


def enter_disease(disease_new):
    data = disease_new
    r = requests.post(url + '/enter-disease', data=data)
    return r.json()


def get_charge(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-charge', params=params)
    return r.json()


def batch_copy_shinryou(visit_id, src_list):
    params = { 'visit-id': visit_id }
    data = src_list
    r = requests.post(url + '/batch-copy-shinryou', params=params, data=data)
    return r.json()


def enter_conduct_shinryou(conduct_shinryou):
    data = conduct_shinryou
    r = requests.post(url + '/enter-conduct-shinryou', data=data)
    return r.json()


def enter_kouhi(kouhi):
    data = kouhi
    r = requests.post(url + '/enter-kouhi', data=data)
    return r.json()


def list_all_presc_example():
    r = requests.get(url + '/list-all-presc-example')
    return r.json()


def finish_cashier(payment):
    data = payment
    r = requests.post(url + '/finish-cashier', data=data)
    return r.json()


def enter_drug_attr(attr):
    data = attr
    r = requests.post(url + '/enter-drug-attr', data=data)
    return r.json()


def enter_drug(drug):
    data = drug
    r = requests.post(url + '/enter-drug', data=data)
    return r.json()


def delete_pharma_drug(iyakuhincode):
    params = { 'iyakuhincode': iyakuhincode }
    r = requests.post(url + '/delete-pharma-drug', params=params)
    return r.json()


def update_patient(patient):
    data = patient
    r = requests.post(url + '/update-patient', data=data)
    return r.json()


def delete_text(text_id):
    params = { 'text-id': text_id }
    r = requests.post(url + '/delete-text', params=params)
    return r.json()


def modify_charge(visit_id, charge):
    params = { 'visit-id': visit_id, 'charge': charge }
    r = requests.post(url + '/modify-charge', params=params)
    return r.json()


def list_available_hoken(patient_id, at):
    params = { 'patient-id': patient_id, 'at': at }
    r = requests.get(url + '/list-available-hoken', params=params)
    return r.json()


def update_drug(drug):
    data = drug
    r = requests.post(url + '/update-drug', data=data)
    return r.json()


def find_gazou_label(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.get(url + '/get-find-label', params=params)
    return r.json()


def delete_conduct_shinryou(conduct_shinryou_id):
    params = { 'conduct-shinryou-id': conduct_shinryou_id }
    r = requests.post(url + '/delete-conduct-shinryou', params=params)
    return r.json()


def list_pharma_queue_for_today():
    r = requests.get(url + '/list-pharma-queue-full-for-today')
    return r.json()


def delete_kouhi(kouhi):
    data = kouhi
    r = requests.post(url + '/delete-kouhi', data=data)
    return r.json()


def enter_hotline(hotline):
    data = hotline
    r = requests.post(url + '/enter-hotline', data=data)
    return r.json()


def list_recent_visits(page, items_per_page):
    params = { 'page': page, 'items-per-page': items_per_page }
    r = requests.get(url + '/list-visit-with-patient', params=params)
    return r.json()


def delete_conduct(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.post(url + '/delete-conduct', params=params)
    return r.json()


def list_pharma_queue_for_prescription():
    r = requests.get(url + '/list-pharma-queue-full-for-prescription')
    return r.json()


def get_drug(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.get(url + '/get-drug', params=params)
    return r.json()


def enter_koukikourei(koukikourei):
    data = koukikourei
    r = requests.post(url + '/enter-koukikourei', data=data)
    return r.json()


def find_shinryou_master_by_name(name, at):
    params = { 'name': name, 'at': at }
    r = requests.get(url + '/find-shinryou-master-by-name', params=params)
    return r.json()


def update_shinryou(shinryou):
    data = shinryou
    r = requests.post(url + '/update-shinryou', data=data)
    return r.json()


def get_patient(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/get-patient', params=params)
    return r.json()


def page_disease_full(patient_id, page, items_per_page):
    params = { 'patient-id': patient_id, 'page': page, 'items-per-page': items_per_page }
    r = requests.get(url + '/page-disease-full', params=params)
    return r.json()


def batch_get_shinryou_attr(shinryou_ids):
    params = { 'shinryou-ids': shinryou_ids }
    r = requests.get(url + '/batch-get-shinryou-attr', params=params)
    return r.json()


def batch_get_shouki(visit_ids):
    params = { 'visit-ids': visit_ids }
    r = requests.get(url + '/batchy-get-shouki', params=params)
    return r.json()


def get_conduct(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.get(url + '/get-conduct', params=params)
    return r.json()


def enter_inject(visit_id, kind, iyakuhincode, amount):
    params = { 'visit-id': visit_id, 'kind': kind, 'iyakuhincode': iyakuhincode, 'amount': amount }
    r = requests.post(url + '/enter-inject', params=params)
    return r.json()


def delete_conduct_drug(conduct_drug_id):
    params = { 'conduct-drug-id': conduct_drug_id }
    r = requests.post(url + '/delete-conduct-drug', params=params)
    return r.json()


def search_presc_example(text):
    params = { 'text': text }
    r = requests.get(url + '/search-presc-example-full-by-name', params=params)
    return r.json()


def search_patient(text):
    params = { 'text': text }
    r = requests.get(url + '/search-patient', params=params)
    return r.json()


def update_koukikourei(koukikourei):
    data = koukikourei
    r = requests.post(url + '/update-koukikourei', data=data)
    return r.json()


def delete_roujin(roujin):
    data = roujin
    r = requests.post(url + '/delete-roujin', data=data)
    return r.json()


def delete_drug_tekiyou(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.post(url + '/delete-drug-tekiyou', params=params)
    return r.json()


def get_master_map_config_file_path():
    r = requests.get(url + '/get-master-map-config-file-path')
    return r.json()


def find_pharma_drug(iyakuhincode):
    params = { 'iyakuhincode': iyakuhincode }
    r = requests.get(url + '/find-pharma-drug', params=params)
    return r.json()


def resolve_shinryoucode(shinryoucode, at):
    params = { 'shinryoucode': shinryoucode, 'at': at }
    r = requests.get(url + '/resolve-shinryoucode', params=params)
    return r.json()


def resolve_iyakuhin_master(iyakuhincode, at):
    params = { 'iyakuhincode': iyakuhincode, 'at': at }
    r = requests.get(url + '/resolve-iyakuhin-master', params=params)
    return r.json()


def list_drug_full(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/list-drug-full', params=params)
    return r.json()


def list_wqueue_full_for_exam():
    r = requests.get(url + '/list-wqueue-full-for-exam')
    return r.json()


def update_shouki(shouki):
    data = shouki
    r = requests.post(url + '/update-shouki', data=data)
    return r.json()


def batch_resolve_byoumei_names(at, args):
    params = { 'at': at }
    data = args
    r = requests.post(url + '/batch-resolve-byoumei-names', params=params, data=data)
    return r.json()


def presc_done(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/presc-done', params=params)
    return r.json()


def search_text_globally(text, page):
    params = { 'text': text, 'page': page }
    r = requests.get(url + '/search-text-globally', params=params)
    return r.json()


def enter_shinryou(shinryou):
    data = shinryou
    r = requests.post(url + '/enter-shinryou', data=data)
    return r.json()


def set_drug_tekiyou(drug_id, tekiyou):
    params = { 'drug-id': drug_id, 'tekiyou': tekiyou }
    r = requests.post(url + '/set-drug-tekiyou', params=params)
    return r.json()


def enter_pharma_drug(pharma_drug):
    data = pharma_drug
    r = requests.post(url + '/enter-pharma-drug', data=data)
    return r.json()


def list_disease_by_patient_at(patient_id, year, month):
    params = { 'patient-id': patient_id, 'year': year, 'month': month }
    r = requests.get(url + '/list-disease-by-patient-at', params=params)
    return r.json()


def get_conduct_full(conduct_id):
    params = { 'conduct-id': conduct_id }
    r = requests.get(url + '/get-conduct-full', params=params)
    return r.json()


def list_iyakuhin_for_patient(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-iyakuhin-for-patient', params=params)
    return r.json()


def search_shuushokugo(text):
    params = { 'text': text }
    r = requests.get(url + '/search-shuushokugo-master', params=params)
    return r.json()


def delete_shahokokuho(shahokokuho):
    data = shahokokuho
    r = requests.post(url + '/delete-shahokokuho', data=data)
    return r.json()


def list_visit_charge_patient_at(at):
    params = { 'at': at }
    r = requests.get(url + '/list-visit-charge-patient-at', params=params)
    return r.json()


def delete_duplicate_shinryou(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/delete-duplicate-shinryou', params=params)
    return r.json()


def get_koukikourei(koukikourei_id):
    params = { 'koukikourei-id': koukikourei_id }
    r = requests.get(url + '/get-koukikourei', params=params)
    return r.json()


def get_shinryou_byoumei_map_config_file_path():
    r = requests.get(url + '/get-shinryou-byoumei-map-config-file-path')
    return r.json()


def search_iyakuhin_master_by_name(text, at):
    params = { 'text': text, 'at': at }
    r = requests.get(url + '/search-iyakuhin-master-by-name', params=params)
    return r.json()


def resolve_shinryou_master(shinryoucode, at):
    params = { 'shinryoucode': shinryoucode, 'at': at }
    r = requests.get(url + '/resolve-shinryou-master', params=params)
    return r.json()


def get_hokensho(patient_id, file):
    params = { 'patient-id': patient_id, 'file': file }
    r = requests.get(url + '/get-hokensho', params=params)
    return r.json()


def delete_shinryou_tekiyou(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.post(url + '/delete-shinryou-tekiyou', params=params)
    return r.json()


def search_text_by_page(patient_id, text, page):
    params = { 'patient-id': patient_id, 'text': text, 'page': page }
    r = requests.get(url + '/search-text-by-page', params=params)
    return r.json()


def page_visit_drug(patient_id, page):
    params = { 'patient-id': patient_id, 'page': page }
    r = requests.get(url + '/page-visit-drug', params=params)
    return r.json()


def get_conduct_drug_full(conduct_drug_id):
    params = { 'conduct-drug-id': conduct_drug_id }
    r = requests.get(url + '/get-conduct-drug-full', params=params)
    return r.json()


def get_visit_meisai(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-visit-meisai', params=params)
    return r.json()


def count_page_of_disease_by_patient(patient_id, items_per_page):
    params = { 'patient-id': patient_id, 'items-per-page': items_per_page }
    r = requests.get(url + '/count-page-of-disease-by-patient', params=params)
    return r.json()


def start_exam(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/start-exam', params=params)
    return r.json()


def get_shinryou_master(shinryoucode, at):
    params = { 'shinryoucode': shinryoucode, 'at': at }
    r = requests.get(url + '/get-shinryou-master', params=params)
    return r.json()


def search_prev_drug(text, patient_id):
    params = { 'text': text, 'patient-id': patient_id }
    r = requests.get(url + '/search-prev-drug', params=params)
    return r.json()


def list_shinryou_full_by_ids(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.get(url + '/list-shinryou-full-by-ids', params=params)
    return r.json()


def start_visit(patient_id, at):
    params = { 'patient-id': patient_id, 'at': at }
    r = requests.post(url + '/start-visit', params=params)
    return r.json()


def modify_disease(disease_modify):
    data = disease_modify
    r = requests.post(url + '/modify-disease', data=data)
    return r.json()


def delete_shinryou(shinryou_id):
    params = { 'shinryou-id': shinryou_id }
    r = requests.post(url + '/delete-shinryou', params=params)
    return r.json()


def list_visit_text_drug_for_patient(patient_id, page):
    params = { 'patient-id': patient_id, 'page': page }
    r = requests.get(url + '/list-visit-text-drug-for-patient', params=params)
    return r.json()


def get_refer_list():
    r = requests.get(url + '/get-refer-list')
    return r.json()


def end_exam(visit_id, charge):
    params = { 'visit-id': visit_id, 'charge': charge }
    r = requests.post(url + '/end-exam', params=params)
    return r.json()


def search_kizai_master(text, at):
    params = { 'text': text, 'at': at }
    r = requests.get(url + '/search-kizai-master-by-name', params=params)
    return r.json()


def batch_resolve_shuushokugo_names(at, args):
    params = { 'at': at }
    data = args
    r = requests.post(url + '/batch-resolve-shuushokugo-names', params=params, data=data)
    return r.json()


def batch_update_disease_end_reason(args):
    data = args
    r = requests.post(url + '/batch-update-disease-end-reason', data=data)
    return r.json()


def list_practice_log_in_range(date, after_id, before_id):
    params = { 'date': date, 'after-id': after_id, 'before-id': before_id }
    r = requests.get(url + '/list-practice-log-in-range', params=params)
    return r.json()


def get_name_map_config_file_path():
    r = requests.get(url + '/get-name-map-config-file-path')
    return r.json()


def get_hoken(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-hoken', params=params)
    return r.json()


def update_kouhi(kouhi):
    data = kouhi
    r = requests.post(url + '/update-kouhi', data=data)
    return r.json()


def suspend_exam(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/suspend-exam', params=params)
    return r.json()


def list_payment_by_patient(patient_id, n):
    params = { 'patient-id': patient_id, 'n': n }
    r = requests.get(url + '/list-payment-by-patient', params=params)
    return r.json()


def list_visiting_patient_id_having_hoken(year, month):
    params = { 'year': year, 'month': month }
    r = requests.get(url + '/list-visiting-patient-id-having-hoken', params=params)
    return r.json()


def update_text(text):
    data = text
    r = requests.post(url + '/update-text', data=data)
    return r.json()


def resolve_kizai_master_by_name(name, at):
    params = { 'name': name, 'at': at }
    r = requests.get(url + '/resolve-kizai-master-by-name', params=params)
    return r.json()


def list_visit_id_by_patient(patient_id):
    params = { 'patient-id': patient_id }
    r = requests.get(url + '/list-visit-id-for-patient', params=params)
    return r.json()


def get_pharma_drug(iyakuhincode):
    params = { 'iyakuhincode': iyakuhincode }
    r = requests.get(url + '/get-pharma-drug', params=params)
    return r.json()


def batch_update_drug_days(drug_id, days):
    params = { 'drug-id': drug_id, 'days': days }
    r = requests.post(url + '/batch-update-drug-days', params=params)
    return r.json()


def delete_drug(drug_id):
    params = { 'drug-id': drug_id }
    r = requests.post(url + '/delete-drug', params=params)
    return r.json()


def get_conduct_shinryou_full(conduct_shinryou_id):
    params = { 'conduct-shinryou-id': conduct_shinryou_id }
    r = requests.get(url + '/get-conduct-shinryou-full', params=params)
    return r.json()


def enter_conduct_drug(conduct_drug):
    data = conduct_drug
    r = requests.post(url + '/enter-conduct-drug', data=data)
    return r.json()


def delete_visit_from_reception(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/delete-visit-from-reception', params=params)
    return r.json()


def copy_all_conducts(target_visit_id, source_visit_id):
    params = { 'target-visit-id': target_visit_id, 'source-visit-id': source_visit_id }
    r = requests.post(url + '/copy-all-conducts', params=params)
    return r.json()


def enter_presc_example(presc_example):
    data = presc_example
    r = requests.post(url + '/enter-presc-example', data=data)
    return r.json()


def delete_presc_example(presc_example_id):
    params = { 'presc-example-id': presc_example_id }
    r = requests.post(url + '/delete-presc-example', params=params)
    return r.json()


def find_shuushokugo_master_by_name(name):
    params = { 'name': name }
    r = requests.get(url + '/find-shuushokugo-master-by-name', params=params)
    return r.json()


def get_name_of_iyakuhin(iyakuhincode):
    params = { 'iyakuhincode': iyakuhincode }
    r = requests.get(url + '/get-name-of-iyakuhin', params=params)
    return r.json()


def set_shinryou_tekiyou(shinryou_id, tekiyou):
    params = { 'shinryou-id': shinryou_id, 'tekiyou': tekiyou }
    r = requests.post(url + '/set-shinryou-tekiyou', params=params)
    return r.json()


def get_visit(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/get-visit', params=params)
    return r.json()


def resolve_kizai_master(kizaicode, at):
    params = { 'kizaicode': kizaicode, 'at': at }
    r = requests.get(url + '/resolve-kizai-master', params=params)
    return r.json()


def modify_gazou_label(conduct_id, label):
    params = { 'conduct-id': conduct_id, 'label': label }
    r = requests.post(url + '/modify-gazou-label', params=params)
    return r.json()


def update_pharma_drug(pharma_drug):
    data = pharma_drug
    r = requests.post(url + '/update-pharma-drug', data=data)
    return r.json()


def get_powder_drug_config_file_path():
    r = requests.get(url + '/get-powder-drug-config-file-path')
    return r.json()


def list_recent_hotline(threshold_hotline_id):
    params = { 'threshold-hotline-id': threshold_hotline_id }
    r = requests.get(url + '/list-recent-hotline', params=params)
    return r.json()


def list_text(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.get(url + '/list-text', params=params)
    return r.json()


def get_roujin(roujin_id):
    params = { 'roujin-id': roujin_id }
    r = requests.get(url + '/get-roujin', params=params)
    return r.json()


def list_all_practice_log(date, last_id):
    params = { 'date': date, 'last-id': last_id }
    r = requests.get(url + '/list-practice-log-after', params=params)
    return r.json()


def list_recent_payment(n):
    params = { 'n': n }
    r = requests.get(url + '/list-recent-payment', params=params)
    return r.json()


def batch_resolve_kizai_names(at, args):
    params = { 'at': at }
    data = args
    r = requests.post(url + '/batch-resolve-kizai-names', params=params, data=data)
    return r.json()


def list_todays_hotline():
    r = requests.get(url + '/list-todays-hotline')
    return r.json()


def resolve_shinryou_master_by_name(name, at):
    params = { 'name': name, 'at': at }
    r = requests.get(url + '/resolve-shinryou-master-by-name', params=params)
    return r.json()


def enter_xp(visit_id, label, film):
    params = { 'visit-id': visit_id, 'label': label, 'film': film }
    r = requests.post(url + '/enter-xp', params=params)
    return r.json()


def enter_shahokokuho(shahokokuho):
    data = shahokokuho
    r = requests.post(url + '/enter-shahokokuho', data=data)
    return r.json()


def update_presc_example(presc_example):
    data = presc_example
    r = requests.post(url + '/update-presc-example', data=data)
    return r.json()


def get_practice_config():
    r = requests.get(url + '/get-practice-config')
    return r.json()


def modify_conduct_kind(conduct_id, kind):
    params = { 'conduct-id': conduct_id, 'kind': kind }
    r = requests.post(url + '/modify-conduct-kind', params=params)
    return r.json()


def enter_patient(patient):
    data = patient
    r = requests.post(url + '/enter-patient', data=data)
    return r.json()


def page_visit_full_with_patient_at(at, page):
    params = { 'at': at, 'page': page }
    r = requests.get(url + '/page-visit-full2-with-patient-at', params=params)
    return r.json()


def update_shahokokuho(shahokokuho):
    data = shahokokuho
    r = requests.post(url + '/update-shahokokuho', data=data)
    return r.json()


def enter_text(text):
    data = text
    r = requests.post(url + '/enter-text', data=data)
    return r.json()


def delete_visit(visit_id):
    params = { 'visit-id': visit_id }
    r = requests.post(url + '/delete-visit', params=params)
    return r.json()


def get_disease_full(disease_id):
    params = { 'disease-id': disease_id }
    r = requests.get(url + '/get-disease-full', params=params)
    return r.json()


