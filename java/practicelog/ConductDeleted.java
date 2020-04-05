package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductDTO;

public class ConductDeleted implements PracticeLogBody {

    public ConductDTO deleted;

    public ConductDeleted() {
    }

    public ConductDeleted(ConductDTO deleted) {
        this.deleted = deleted;
    }
}