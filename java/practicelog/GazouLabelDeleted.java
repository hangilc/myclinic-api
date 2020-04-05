package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.GazouLabelDTO;

public class GazouLabelDeleted implements PracticeLogBody {

    public GazouLabelDTO deleted;

    public GazouLabelDeleted() {
    }

    public GazouLabelDeleted(GazouLabelDTO deleted) {
        this.deleted = deleted;
    }
}