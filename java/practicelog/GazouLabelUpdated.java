package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.GazouLabelDTO;

public class GazouLabelUpdated implements PracticeLogBody {

    public GazouLabelDTO prev;
    public GazouLabelDTO updated;

    public GazouLabelUpdated() {
    }

    public GazouLabelUpdated(GazouLabelDTO prev, GazouLabelDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}