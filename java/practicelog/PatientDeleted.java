package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PatientDTO;

public class PatientDeleted implements PracticeLogBody {

    public PatientDTO deleted;

    public PatientDeleted() {
    }

    public PatientDeleted(PatientDTO deleted) {
        this.deleted = deleted;
    }
}
