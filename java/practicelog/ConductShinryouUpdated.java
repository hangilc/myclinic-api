package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ConductShinryouDTO;

public class ConductShinryouUpdated implements PracticeLogBody {

    public ConductShinryouDTO prev;
    public ConductShinryouDTO updated;

    public ConductShinryouUpdated() {
    }

    public ConductShinryouUpdated(ConductShinryouDTO prev, ConductShinryouDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}