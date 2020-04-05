package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.WqueueDTO;

public class WqueueCreated implements PracticeLogBody {

    public WqueueDTO created;

    public WqueueCreated() {
    }

    public WqueueCreated(WqueueDTO created) {
        this.created = created;
    }
}
