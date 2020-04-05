package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDTO;

public class ConductUpdated implements PracticeLogBody {

    public ConductDTO prev;
    public ConductDTO updated;

    public ConductUpdated() {
    }

    public ConductUpdated(ConductDTO prev, ConductDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}