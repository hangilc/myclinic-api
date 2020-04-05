package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductShinryouDTO;

public class ConductShinryouDeleted implements PracticeLogBody {

    public ConductShinryouDTO deleted;

    public ConductShinryouDeleted() {
    }

    public ConductShinryouDeleted(ConductShinryouDTO deleted) {
        this.deleted = deleted;
    }
}