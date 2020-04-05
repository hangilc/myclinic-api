package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductShinryouDTO;

public class ConductShinryouCreated implements PracticeLogBody {

    public ConductShinryouDTO created;

    public ConductShinryouCreated() {
    }

    public ConductShinryouCreated(ConductShinryouDTO created) {
        this.created = created;
    }
}