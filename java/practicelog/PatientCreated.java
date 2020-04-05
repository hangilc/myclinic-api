package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PatientDTO;

public class PatientCreated implements PracticeLogBody {

    public PatientDTO created;

    public PatientCreated() {
    }

    public PatientCreated(PatientDTO created) {
        this.created = created;
    }
}
