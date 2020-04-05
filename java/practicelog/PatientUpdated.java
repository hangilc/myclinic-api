package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PatientDTO;

public class PatientUpdated implements PracticeLogBody {

    public PatientDTO prev;
    public PatientDTO updated;

    public PatientUpdated() {
    }

    public PatientUpdated(PatientDTO prev, PatientDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
