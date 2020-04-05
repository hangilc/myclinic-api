package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.WqueueDTO;

public class WqueueDeleted implements PracticeLogBody {

    public WqueueDTO deleted;

    public WqueueDeleted() {
    }

    public WqueueDeleted(WqueueDTO deleted) {
        this.deleted = deleted;
    }
}
