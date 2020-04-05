
from server_app import (
    app, request, Session, jsonify, impl, ImplementationError, model,
    confirm_str, send_file, MyclinicContext, 
    enter_myclinic_logs, emit_myclinic_logs
)



@app.route("/json/search-byoumei-master", methods=["GET"])
def search_byoumei():
    text = request.args.get('text')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.search_byoumei(session, text, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-visit-by-patient-having-hoken", methods=["GET"])
def list_visit_by_patient_having_hoken():
    patient_id = int(request.args.get('patient-id'))
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_by_patient_having_hoken(session, patient_id, year, month))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-recently-registered-patients", methods=["GET"])
def list_recently_registered_patients():
    n = None if request.args.get('n') is None else int(request.args.get('n'))
    
    session = Session()
    try:
        result = jsonify(impl.list_recently_registered_patients(session, n))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-todays-hotline-in-range", methods=["GET"])
def list_todays_hotline_in_range():
    after = int(request.args.get('after'))
    before = int(request.args.get('before'))
    
    session = Session()
    try:
        result = jsonify(impl.list_todays_hotline_in_range(session, after, before))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-todays-visits", methods=["GET"])
def list_todays_visits():
    
    session = Session()
    try:
        result = jsonify(impl.list_todays_visits(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-get-drug-attr", methods=["GET"])
def batch_get_drug_attr():
    drug_ids = [int(x) for x in request.args.getlist('drug-ids')]
    
    session = Session()
    try:
        result = jsonify(impl.batch_get_drug_attr(session, drug_ids))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-drug-full", methods=["GET"])
def get_drug_full():
    drug_id = int(request.args.get('drug-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_drug_full(session, drug_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-shinryou-full", methods=["GET"])
def get_shinryou_full():
    shinryou_id = int(request.args.get('shinryou-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_shinryou_full(session, shinryou_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/convert-to-hoken", methods=["POST"])
def convert_to_hoken():
    visit = model.Visit.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.convert_to_hoken(session, visit))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/batch-delete-drugs", methods=["POST"])
def batch_delete_drugs():
    drug_id = [int(x) for x in request.args.getlist('drug-id')]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_delete_drugs(session, drug_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-conduct-kizai-full", methods=["GET"])
def get_conduct_kizai_full():
    conduct_kizai_id = int(request.args.get('conduct-kizai-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_conduct_kizai_full(session, conduct_kizai_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/find-byoumei-master-by-name", methods=["GET"])
def find_byoumei_master_by_name():
    name = request.args.get('name')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.find_byoumei_master_by_name(session, name, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-disease-example", methods=["GET"])
def list_disease_example():
    return jsonify(impl.list_disease_example())
        
    

@app.route("/json/list-drug-full-by-drug-ids", methods=["GET"])
def list_drug_full_by_drug_ids():
    drug_id = [int(x) for x in request.args.getlist('drug-id')]
    
    session = Session()
    try:
        result = jsonify(impl.list_drug_full_by_drug_ids(session, drug_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-wqueue-full", methods=["GET"])
def list_wqueue_full():
    
    session = Session()
    try:
        result = jsonify(impl.list_wqueue_full(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-shahokokuho", methods=["GET"])
def get_shahokokuho():
    shahokokuho_id = int(request.args.get('shahokokuho-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_shahokokuho(session, shahokokuho_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-resolve-shinryou-names", methods=["POST"])
def batch_resolve_shinryou_names():
    at = request.args.get('at')
    args = [[confirm_str(x) for x in x] for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_resolve_shinryou_names(session, at, args))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-conduct-kizai", methods=["POST"])
def delete_conduct_kizai():
    conduct_kizai_id = int(request.args.get('conduct-kizai-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_conduct_kizai(session, conduct_kizai_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-pharma-queue-full", methods=["GET"])
def get_pharma_queue_full():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_pharma_queue_full(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-shinryou-attr", methods=["POST"])
def enter_shinryou_attr():
    attr = model.ShinryouAttr.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_shinryou_attr(session, attr))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-gazou-label", methods=["POST"])
def delete_gazou_label():
    conduct_id = int(request.args.get('conduct-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_gazou_label(session, conduct_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/find-shinryou-attr", methods=["GET"])
def find_shinryou_attr():
    shinryou_id = int(request.args.get('shinryou-id'))
    
    session = Session()
    try:
        result = jsonify(impl.find_shinryou_attr(session, shinryou_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-visit-full2", methods=["GET"])
def list_visit_full_2():
    patient_id = int(request.args.get('patient-id'))
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_full_2(session, patient_id, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-text", methods=["GET"])
def get_text():
    text_id = int(request.args.get('text-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_text(session, text_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-conduct-full", methods=["POST"])
def enter_conduct_full():
    arg = model.ConductEnterRequest.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_conduct_full(session, arg))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/find-shouki", methods=["GET"])
def find_shouki():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.find_shouki(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-conduct-full-by-ids", methods=["GET"])
def list_conduct_full_by_ids():
    conduct_id = [int(x) for x in request.args.getlist('conduct-id')]
    
    session = Session()
    try:
        result = jsonify(impl.list_conduct_full_by_ids(session, conduct_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-kouhi", methods=["GET"])
def get_kouhi():
    kouhi_id = int(request.args.get('kouhi-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_kouhi(session, kouhi_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-shouki", methods=["POST"])
def enter_shouki():
    shouki = model.Shouki.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_shouki(session, shouki))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-hokensho", methods=["GET"])
def list_hokensho():
    patient_id = int(request.args.get('patient-id'))
    return jsonify(impl.list_hokensho(patient_id))
        
    

@app.route("/json/delete-koukikourei", methods=["POST"])
def delete_koukikourei():
    koukikourei = model.Koukikourei.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_koukikourei(session, koukikourei))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-disease-full", methods=["GET"])
def list_disease_full():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_disease_full(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-hoken", methods=["GET"])
def list_hoken():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_hoken(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-shouki", methods=["POST"])
def delete_shouki():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_shouki(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/find-drug-attr", methods=["GET"])
def find_drug_attr():
    drug_id = int(request.args.get('drug-id'))
    
    session = Session()
    try:
        result = jsonify(impl.find_drug_attr(session, drug_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-hoken", methods=["POST"])
def update_hoken():
    hoken = model.UpdateHoken.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_hoken(session, hoken))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-visit-text-drug-by-patient-and-iyakuhincode", methods=["GET"])
def list_visit_text_drug_by_patient_and_iyakuhincode():
    patient_id = int(request.args.get('patient-id'))
    iyakuhincode = int(request.args.get('iyakuhincode'))
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_text_drug_by_patient_and_iyakuhincode(session, patient_id, iyakuhincode, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-wqueue-full", methods=["GET"])
def get_wqueue_full():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_wqueue_full(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-shinryou-full", methods=["GET"])
def list_shinryou_full():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_shinryou_full(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/search-shinryou-master", methods=["GET"])
def search_shinryou_master():
    text = request.args.get('text')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.search_shinryou_master(session, text, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-enter-shinryou-by-name", methods=["POST"])
def batch_enter_shinryou_by_name():
    name = [x for x in request.args.getlist('name')]
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_enter_shinryou_by_name(session, name, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-conduct-kizai", methods=["POST"])
def enter_conduct_kizai():
    conduct_kizai = model.ConductKizai.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_conduct_kizai(session, conduct_kizai))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/batch-enter-drugs", methods=["POST"])
def batch_enter_drugs():
    drugs = [model.Drug.from_dict(x) for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_enter_drugs(session, drugs))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-disease", methods=["POST"])
def delete_disease():
    disease_id = int(request.args.get('disease-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_disease(session, disease_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/batch-resolve-iyakuhin-master", methods=["GET"])
def batch_resolve_iyakuhin_master():
    iyakuhincode = [int(x) for x in request.args.getlist('iyakuhincode')]
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.batch_resolve_iyakuhin_master(session, iyakuhincode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-clinic-info", methods=["GET"])
def get_clinic_info():
    return jsonify(impl.get_clinic_info())
        
    

@app.route("/json/list-all-pharma-drug-names", methods=["GET"])
def list_all_pharma_drug_names():
    
    session = Session()
    try:
        result = jsonify(impl.list_all_pharma_drug_names(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-payment", methods=["GET"])
def list_payment():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_payment(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-visit-id-visited-at-by-patient-and-iyakuhincode", methods=["GET"])
def list_visit_id_visited_at_by_patient_and_iyakuhincode():
    patient_id = int(request.args.get('patient-id'))
    iyakuhincode = int(request.args.get('iyakuhincode'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_id_visited_at_by_patient_and_iyakuhincode(session, patient_id, iyakuhincode))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-delete-shinryou", methods=["POST"])
def batch_delete_shinryou():
    shinryou_id = [int(x) for x in request.args.getlist('shinryou-id')]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_delete_shinryou(session, shinryou_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-current-disease-full", methods=["GET"])
def list_current_disease_full():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_current_disease_full(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-disease", methods=["POST"])
def enter_disease():
    disease_new = model.DiseaseNew.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_disease(session, disease_new))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-charge", methods=["GET"])
def get_charge():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_charge(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-copy-shinryou", methods=["POST"])
def batch_copy_shinryou():
    visit_id = int(request.args.get('visit-id'))
    src_list = [model.Shinryou.from_dict(x) for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_copy_shinryou(session, visit_id, src_list))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-conduct-shinryou", methods=["POST"])
def enter_conduct_shinryou():
    conduct_shinryou = model.ConductShinryou.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_conduct_shinryou(session, conduct_shinryou))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-kouhi", methods=["POST"])
def enter_kouhi():
    kouhi = model.Kouhi.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_kouhi(session, kouhi))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-all-presc-example", methods=["GET"])
def list_all_presc_example():
    
    session = Session()
    try:
        result = jsonify(impl.list_all_presc_example(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/finish-cashier", methods=["POST"])
def finish_cashier():
    payment = model.Payment.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.finish_cashier(session, payment))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-drug-attr", methods=["POST"])
def enter_drug_attr():
    attr = model.DrugAttr.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_drug_attr(session, attr))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-drug", methods=["POST"])
def enter_drug():
    drug = model.Drug.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_drug(session, drug))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-pharma-drug", methods=["POST"])
def delete_pharma_drug():
    iyakuhincode = int(request.args.get('iyakuhincode'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_pharma_drug(session, iyakuhincode))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/update-patient", methods=["POST"])
def update_patient():
    patient = model.Patient.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_patient(session, patient))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-text", methods=["POST"])
def delete_text():
    text_id = int(request.args.get('text-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_text(session, text_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/modify-charge", methods=["POST"])
def modify_charge():
    visit_id = int(request.args.get('visit-id'))
    charge = int(request.args.get('charge'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.modify_charge(session, visit_id, charge))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-available-hoken", methods=["GET"])
def list_available_hoken():
    patient_id = int(request.args.get('patient-id'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.list_available_hoken(session, patient_id, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-drug", methods=["POST"])
def update_drug():
    drug = model.Drug.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_drug(session, drug))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-find-label", methods=["GET"])
def find_gazou_label():
    conduct_id = int(request.args.get('conduct-id'))
    
    session = Session()
    try:
        result = jsonify(impl.find_gazou_label(session, conduct_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-conduct-shinryou", methods=["POST"])
def delete_conduct_shinryou():
    conduct_shinryou_id = int(request.args.get('conduct-shinryou-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_conduct_shinryou(session, conduct_shinryou_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-pharma-queue-full-for-today", methods=["GET"])
def list_pharma_queue_for_today():
    
    session = Session()
    try:
        result = jsonify(impl.list_pharma_queue_for_today(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-kouhi", methods=["POST"])
def delete_kouhi():
    kouhi = model.Kouhi.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_kouhi(session, kouhi))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-hotline", methods=["POST"])
def enter_hotline():
    hotline = model.Hotline.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_hotline(session, hotline))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-visit-with-patient", methods=["GET"])
def list_recent_visits():
    page = None if request.args.get('page') is None else int(request.args.get('page'))
    items_per_page = None if request.args.get('items-per-page') is None else int(request.args.get('items-per-page'))
    
    session = Session()
    try:
        result = jsonify(impl.list_recent_visits(session, page, items_per_page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-conduct", methods=["POST"])
def delete_conduct():
    conduct_id = int(request.args.get('conduct-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_conduct(session, conduct_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-pharma-queue-full-for-prescription", methods=["GET"])
def list_pharma_queue_for_prescription():
    
    session = Session()
    try:
        result = jsonify(impl.list_pharma_queue_for_prescription(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-drug", methods=["GET"])
def get_drug():
    drug_id = int(request.args.get('drug-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_drug(session, drug_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-koukikourei", methods=["POST"])
def enter_koukikourei():
    koukikourei = model.Koukikourei.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_koukikourei(session, koukikourei))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/find-shinryou-master-by-name", methods=["GET"])
def find_shinryou_master_by_name():
    name = request.args.get('name')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.find_shinryou_master_by_name(session, name, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-shinryou", methods=["POST"])
def update_shinryou():
    shinryou = model.Shinryou.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_shinryou(session, shinryou))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-patient", methods=["GET"])
def get_patient():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_patient(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/page-disease-full", methods=["GET"])
def page_disease_full():
    patient_id = int(request.args.get('patient-id'))
    page = int(request.args.get('page'))
    items_per_page = int(request.args.get('items-per-page'))
    
    session = Session()
    try:
        result = jsonify(impl.page_disease_full(session, patient_id, page, items_per_page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-get-shinryou-attr", methods=["GET"])
def batch_get_shinryou_attr():
    shinryou_ids = [int(x) for x in request.args.getlist('shinryou-ids')]
    
    session = Session()
    try:
        result = jsonify(impl.batch_get_shinryou_attr(session, shinryou_ids))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batchy-get-shouki", methods=["GET"])
def batch_get_shouki():
    visit_ids = [int(x) for x in request.args.getlist('visit-ids')]
    
    session = Session()
    try:
        result = jsonify(impl.batch_get_shouki(session, visit_ids))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-conduct", methods=["GET"])
def get_conduct():
    conduct_id = int(request.args.get('conduct-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_conduct(session, conduct_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-inject", methods=["POST"])
def enter_inject():
    visit_id = int(request.args.get('visit-id'))
    kind = int(request.args.get('kind'))
    iyakuhincode = int(request.args.get('iyakuhincode'))
    amount = float(request.args.get('amount'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_inject(session, visit_id, kind, iyakuhincode, amount))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-conduct-drug", methods=["POST"])
def delete_conduct_drug():
    conduct_drug_id = int(request.args.get('conduct-drug-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_conduct_drug(session, conduct_drug_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/search-presc-example-full-by-name", methods=["GET"])
def search_presc_example():
    text = request.args.get('text')
    
    session = Session()
    try:
        result = jsonify(impl.search_presc_example(session, text))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/search-patient", methods=["GET"])
def search_patient():
    text = request.args.get('text')
    
    session = Session()
    try:
        result = jsonify(impl.search_patient(session, text))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-koukikourei", methods=["POST"])
def update_koukikourei():
    koukikourei = model.Koukikourei.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_koukikourei(session, koukikourei))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-roujin", methods=["POST"])
def delete_roujin():
    roujin = model.Roujin.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_roujin(session, roujin))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-drug-tekiyou", methods=["POST"])
def delete_drug_tekiyou():
    drug_id = int(request.args.get('drug-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_drug_tekiyou(session, drug_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-master-map-config-file-path", methods=["GET"])
def get_master_map_config_file_path():
    return jsonify(impl.get_master_map_config_file_path())
        
    

@app.route("/json/find-pharma-drug", methods=["GET"])
def find_pharma_drug():
    iyakuhincode = int(request.args.get('iyakuhincode'))
    
    session = Session()
    try:
        result = jsonify(impl.find_pharma_drug(session, iyakuhincode))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/resolve-shinryoucode", methods=["GET"])
def resolve_shinryoucode():
    shinryoucode = int(request.args.get('shinryoucode'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_shinryoucode(session, shinryoucode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/resolve-iyakuhin-master", methods=["GET"])
def resolve_iyakuhin_master():
    iyakuhincode = int(request.args.get('iyakuhincode'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_iyakuhin_master(session, iyakuhincode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-drug-full", methods=["GET"])
def list_drug_full():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_drug_full(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-wqueue-full-for-exam", methods=["GET"])
def list_wqueue_full_for_exam():
    
    session = Session()
    try:
        result = jsonify(impl.list_wqueue_full_for_exam(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-shouki", methods=["POST"])
def update_shouki():
    shouki = model.Shouki.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_shouki(session, shouki))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/batch-resolve-byoumei-names", methods=["POST"])
def batch_resolve_byoumei_names():
    at = request.args.get('at')
    args = [[confirm_str(x) for x in x] for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_resolve_byoumei_names(session, at, args))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/presc-done", methods=["POST"])
def presc_done():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.presc_done(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/search-text-globally", methods=["GET"])
def search_text_globally():
    text = request.args.get('text')
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.search_text_globally(session, text, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-shinryou", methods=["POST"])
def enter_shinryou():
    shinryou = model.Shinryou.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_shinryou(session, shinryou))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/set-drug-tekiyou", methods=["POST"])
def set_drug_tekiyou():
    drug_id = int(request.args.get('drug-id'))
    tekiyou = request.args.get('tekiyou')
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.set_drug_tekiyou(session, drug_id, tekiyou))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-pharma-drug", methods=["POST"])
def enter_pharma_drug():
    pharma_drug = model.PharmaDrug.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_pharma_drug(session, pharma_drug))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-disease-by-patient-at", methods=["GET"])
def list_disease_by_patient_at():
    patient_id = int(request.args.get('patient-id'))
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    
    session = Session()
    try:
        result = jsonify(impl.list_disease_by_patient_at(session, patient_id, year, month))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-conduct-full", methods=["GET"])
def get_conduct_full():
    conduct_id = int(request.args.get('conduct-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_conduct_full(session, conduct_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-iyakuhin-for-patient", methods=["GET"])
def list_iyakuhin_for_patient():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_iyakuhin_for_patient(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/search-shuushokugo-master", methods=["GET"])
def search_shuushokugo():
    text = request.args.get('text')
    
    session = Session()
    try:
        result = jsonify(impl.search_shuushokugo(session, text))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-shahokokuho", methods=["POST"])
def delete_shahokokuho():
    shahokokuho = model.Shahokokuho.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_shahokokuho(session, shahokokuho))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-visit-charge-patient-at", methods=["GET"])
def list_visit_charge_patient_at():
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_charge_patient_at(session, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/delete-duplicate-shinryou", methods=["POST"])
def delete_duplicate_shinryou():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_duplicate_shinryou(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-koukikourei", methods=["GET"])
def get_koukikourei():
    koukikourei_id = int(request.args.get('koukikourei-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_koukikourei(session, koukikourei_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-shinryou-byoumei-map-config-file-path", methods=["GET"])
def get_shinryou_byoumei_map_config_file_path():
    return jsonify(impl.get_shinryou_byoumei_map_config_file_path())
        
    

@app.route("/json/search-iyakuhin-master-by-name", methods=["GET"])
def search_iyakuhin_master_by_name():
    text = request.args.get('text')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.search_iyakuhin_master_by_name(session, text, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/resolve-shinryou-master", methods=["GET"])
def resolve_shinryou_master():
    shinryoucode = int(request.args.get('shinryoucode'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_shinryou_master(session, shinryoucode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-hokensho", methods=["GET"])
def get_hokensho():
    patient_id = int(request.args.get('patient-id'))
    file = request.args.get('file')
    kwargs = impl.get_hokensho(patient_id, file)
    return send_file(**kwargs)
        
    

@app.route("/json/delete-shinryou-tekiyou", methods=["POST"])
def delete_shinryou_tekiyou():
    shinryou_id = int(request.args.get('shinryou-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_shinryou_tekiyou(session, shinryou_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/search-text-by-page", methods=["GET"])
def search_text_by_page():
    patient_id = int(request.args.get('patient-id'))
    text = request.args.get('text')
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.search_text_by_page(session, patient_id, text, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/page-visit-drug", methods=["GET"])
def page_visit_drug():
    patient_id = int(request.args.get('patient-id'))
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.page_visit_drug(session, patient_id, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-conduct-drug-full", methods=["GET"])
def get_conduct_drug_full():
    conduct_drug_id = int(request.args.get('conduct-drug-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_conduct_drug_full(session, conduct_drug_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-visit-meisai", methods=["GET"])
def get_visit_meisai():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_visit_meisai(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/count-page-of-disease-by-patient", methods=["GET"])
def count_page_of_disease_by_patient():
    patient_id = int(request.args.get('patient-id'))
    items_per_page = int(request.args.get('items-per-page'))
    
    session = Session()
    try:
        result = jsonify(impl.count_page_of_disease_by_patient(session, patient_id, items_per_page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/start-exam", methods=["POST"])
def start_exam():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.start_exam(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-shinryou-master", methods=["GET"])
def get_shinryou_master():
    shinryoucode = int(request.args.get('shinryoucode'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.get_shinryou_master(session, shinryoucode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/search-prev-drug", methods=["GET"])
def search_prev_drug():
    text = None if request.args.get('text') is None else request.args.get('text')
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.search_prev_drug(session, text, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-shinryou-full-by-ids", methods=["GET"])
def list_shinryou_full_by_ids():
    shinryou_id = [int(x) for x in request.args.getlist('shinryou-id')]
    
    session = Session()
    try:
        result = jsonify(impl.list_shinryou_full_by_ids(session, shinryou_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/start-visit", methods=["POST"])
def start_visit():
    patient_id = int(request.args.get('patient-id'))
    at = None if request.args.get('at') is None else request.args.get('at')
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.start_visit(session, patient_id, at))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/modify-disease", methods=["POST"])
def modify_disease():
    disease_modify = model.DiseaseModify.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.modify_disease(session, disease_modify))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-shinryou", methods=["POST"])
def delete_shinryou():
    shinryou_id = int(request.args.get('shinryou-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_shinryou(session, shinryou_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-visit-text-drug-for-patient", methods=["GET"])
def list_visit_text_drug_for_patient():
    patient_id = int(request.args.get('patient-id'))
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_text_drug_for_patient(session, patient_id, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-refer-list", methods=["GET"])
def get_refer_list():
    return jsonify(impl.get_refer_list())
        
    

@app.route("/json/end-exam", methods=["POST"])
def end_exam():
    visit_id = int(request.args.get('visit-id'))
    charge = int(request.args.get('charge'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.end_exam(session, visit_id, charge))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/search-kizai-master-by-name", methods=["GET"])
def search_kizai_master():
    text = request.args.get('text')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.search_kizai_master(session, text, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-resolve-shuushokugo-names", methods=["POST"])
def batch_resolve_shuushokugo_names():
    at = request.args.get('at')
    args = [[confirm_str(x) for x in x] for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_resolve_shuushokugo_names(session, at, args))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/batch-update-disease-end-reason", methods=["POST"])
def batch_update_disease_end_reason():
    args = [model.DiseaseModifyEndReason.from_dict(x) for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_update_disease_end_reason(session, args))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-practice-log-in-range", methods=["GET"])
def list_practice_log_in_range():
    date = request.args.get('date')
    after_id = int(request.args.get('after-id'))
    before_id = int(request.args.get('before-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_practice_log_in_range(session, date, after_id, before_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-name-map-config-file-path", methods=["GET"])
def get_name_map_config_file_path():
    return jsonify(impl.get_name_map_config_file_path())
        
    

@app.route("/json/get-hoken", methods=["GET"])
def get_hoken():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_hoken(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-kouhi", methods=["POST"])
def update_kouhi():
    kouhi = model.Kouhi.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_kouhi(session, kouhi))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/suspend-exam", methods=["POST"])
def suspend_exam():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.suspend_exam(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-payment-by-patient", methods=["GET"])
def list_payment_by_patient():
    patient_id = int(request.args.get('patient-id'))
    n = None if request.args.get('n') is None else int(request.args.get('n'))
    
    session = Session()
    try:
        result = jsonify(impl.list_payment_by_patient(session, patient_id, n))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-visiting-patient-id-having-hoken", methods=["GET"])
def list_visiting_patient_id_having_hoken():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visiting_patient_id_having_hoken(session, year, month))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-text", methods=["POST"])
def update_text():
    text = model.Text.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_text(session, text))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/resolve-kizai-master-by-name", methods=["GET"])
def resolve_kizai_master_by_name():
    name = request.args.get('name')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_kizai_master_by_name(session, name, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-visit-id-for-patient", methods=["GET"])
def list_visit_id_by_patient():
    patient_id = int(request.args.get('patient-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_visit_id_by_patient(session, patient_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-pharma-drug", methods=["GET"])
def get_pharma_drug():
    iyakuhincode = int(request.args.get('iyakuhincode'))
    
    session = Session()
    try:
        result = jsonify(impl.get_pharma_drug(session, iyakuhincode))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-update-drug-days", methods=["POST"])
def batch_update_drug_days():
    drug_id = [int(x) for x in request.args.getlist('drug-id')]
    days = int(request.args.get('days'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_update_drug_days(session, drug_id, days))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-drug", methods=["POST"])
def delete_drug():
    drug_id = int(request.args.get('drug-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_drug(session, drug_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-conduct-shinryou-full", methods=["GET"])
def get_conduct_shinryou_full():
    conduct_shinryou_id = int(request.args.get('conduct-shinryou-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_conduct_shinryou_full(session, conduct_shinryou_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-conduct-drug", methods=["POST"])
def enter_conduct_drug():
    conduct_drug = model.ConductDrug.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_conduct_drug(session, conduct_drug))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-visit-from-reception", methods=["POST"])
def delete_visit_from_reception():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_visit_from_reception(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/copy-all-conducts", methods=["POST"])
def copy_all_conducts():
    target_visit_id = int(request.args.get('target-visit-id'))
    source_visit_id = int(request.args.get('source-visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.copy_all_conducts(session, target_visit_id, source_visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-presc-example", methods=["POST"])
def enter_presc_example():
    presc_example = model.PrescExample.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_presc_example(session, presc_example))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-presc-example", methods=["POST"])
def delete_presc_example():
    presc_example_id = int(request.args.get('presc-example-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_presc_example(session, presc_example_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/find-shuushokugo-master-by-name", methods=["GET"])
def find_shuushokugo_master_by_name():
    name = request.args.get('name')
    
    session = Session()
    try:
        result = jsonify(impl.find_shuushokugo_master_by_name(session, name))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-name-of-iyakuhin", methods=["GET"])
def get_name_of_iyakuhin():
    iyakuhincode = int(request.args.get('iyakuhincode'))
    
    session = Session()
    try:
        result = jsonify(impl.get_name_of_iyakuhin(session, iyakuhincode))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/set-shinryou-tekiyou", methods=["POST"])
def set_shinryou_tekiyou():
    shinryou_id = int(request.args.get('shinryou-id'))
    tekiyou = request.args.get('tekiyou')
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.set_shinryou_tekiyou(session, shinryou_id, tekiyou))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-visit", methods=["GET"])
def get_visit():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_visit(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/resolve-kizai-master", methods=["GET"])
def resolve_kizai_master():
    kizaicode = int(request.args.get('kizaicode'))
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_kizai_master(session, kizaicode, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/modify-gazou-label", methods=["POST"])
def modify_gazou_label():
    conduct_id = int(request.args.get('conduct-id'))
    label = request.args.get('label')
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.modify_gazou_label(session, conduct_id, label))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/update-pharma-drug", methods=["POST"])
def update_pharma_drug():
    pharma_drug = model.PharmaDrug.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_pharma_drug(session, pharma_drug))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-powder-drug-config-file-path", methods=["GET"])
def get_powder_drug_config_file_path():
    return jsonify(impl.get_powder_drug_config_file_path())
        
    

@app.route("/json/list-recent-hotline", methods=["GET"])
def list_recent_hotline():
    threshold_hotline_id = int(request.args.get('threshold-hotline-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_recent_hotline(session, threshold_hotline_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-text", methods=["GET"])
def list_text():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_text(session, visit_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/get-roujin", methods=["GET"])
def get_roujin():
    roujin_id = int(request.args.get('roujin-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_roujin(session, roujin_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-practice-log-after", methods=["GET"])
def list_all_practice_log():
    date = request.args.get('date')
    last_id = int(request.args.get('last-id'))
    
    session = Session()
    try:
        result = jsonify(impl.list_all_practice_log(session, date, last_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/list-recent-payment", methods=["GET"])
def list_recent_payment():
    n = None if request.args.get('n') is None else int(request.args.get('n'))
    
    session = Session()
    try:
        result = jsonify(impl.list_recent_payment(session, n))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/batch-resolve-kizai-names", methods=["POST"])
def batch_resolve_kizai_names():
    at = request.args.get('at')
    args = [[confirm_str(x) for x in x] for x in request.get_json(force=True)]
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.batch_resolve_kizai_names(session, at, args))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/list-todays-hotline", methods=["GET"])
def list_todays_hotline():
    
    session = Session()
    try:
        result = jsonify(impl.list_todays_hotline(session))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/resolve-shinryou-master-by-name", methods=["GET"])
def resolve_shinryou_master_by_name():
    name = request.args.get('name')
    at = request.args.get('at')
    
    session = Session()
    try:
        result = jsonify(impl.resolve_shinryou_master_by_name(session, name, at))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/enter-xp", methods=["POST"])
def enter_xp():
    visit_id = int(request.args.get('visit-id'))
    label = request.args.get('label')
    film = request.args.get('film')
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_xp(session, visit_id, label, film))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-shahokokuho", methods=["POST"])
def enter_shahokokuho():
    shahokokuho = model.Shahokokuho.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_shahokokuho(session, shahokokuho))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/update-presc-example", methods=["POST"])
def update_presc_example():
    presc_example = model.PrescExample.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_presc_example(session, presc_example))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-practice-config", methods=["GET"])
def get_practice_config():
    return jsonify(impl.get_practice_config())
        
    

@app.route("/json/modify-conduct-kind", methods=["POST"])
def modify_conduct_kind():
    conduct_id = int(request.args.get('conduct-id'))
    kind = int(request.args.get('kind'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.modify_conduct_kind(session, conduct_id, kind))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-patient", methods=["POST"])
def enter_patient():
    patient = model.Patient.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_patient(session, patient))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/page-visit-full2-with-patient-at", methods=["GET"])
def page_visit_full_with_patient_at():
    at = request.args.get('at')
    page = int(request.args.get('page'))
    
    session = Session()
    try:
        result = jsonify(impl.page_visit_full_with_patient_at(session, at, page))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    

@app.route("/json/update-shahokokuho", methods=["POST"])
def update_shahokokuho():
    shahokokuho = model.Shahokokuho.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.update_shahokokuho(session, shahokokuho))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/enter-text", methods=["POST"])
def enter_text():
    text = model.Text.from_dict(request.get_json(force=True))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.enter_text(session, text))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/delete-visit", methods=["POST"])
def delete_visit():
    visit_id = int(request.args.get('visit-id'))
    
    session = Session()
    session.myclinic = MyclinicContext()
    try:
        result = jsonify(impl.delete_visit(session, visit_id))
        session.flush()
        enter_myclinic_logs(session)
        session.commit()
        emit_myclinic_logs(session)
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        del session.myclinic
        session.close()
    

@app.route("/json/get-disease-full", methods=["GET"])
def get_disease_full():
    disease_id = int(request.args.get('disease-id'))
    
    session = Session()
    try:
        result = jsonify(impl.get_disease_full(session, disease_id))
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise ImplementationError(str(e))
    finally:
        session.close()
    


def init_routes():
    pass

