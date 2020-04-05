package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.PharmaQueueDTO;

public class PharmaQueueUpdated implements PracticeLogBody {

    public PharmaQueueDTO prev;
    public PharmaQueueDTO updated;

    public PharmaQueueUpdated() {
    }

    public PharmaQueueUpdated(PharmaQueueDTO prev, PharmaQueueDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
