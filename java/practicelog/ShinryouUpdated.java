package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ShinryouDTO;

public class ShinryouUpdated implements PracticeLogBody {

    public ShinryouDTO prev;
    public ShinryouDTO updated;

    public ShinryouUpdated() {
    }

    public ShinryouUpdated(ShinryouDTO prev, ShinryouDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}