package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.WqueueDTO;

public class WqueueUpdated implements PracticeLogBody {

    public WqueueDTO prev;
    public WqueueDTO updated;

    public WqueueUpdated() {
    }

    public WqueueUpdated(WqueueDTO prev, WqueueDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
