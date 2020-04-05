package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDTO;

public class ConductCreated implements PracticeLogBody {

    public ConductDTO created;

    public ConductCreated() {
    }

    public ConductCreated(ConductDTO created) {
        this.created = created;
    }
}