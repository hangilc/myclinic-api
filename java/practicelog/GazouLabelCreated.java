package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.GazouLabelDTO;

public class GazouLabelCreated implements PracticeLogBody {

    public GazouLabelDTO created;

    public GazouLabelCreated() {
    }

    public GazouLabelCreated(GazouLabelDTO created) {
        this.created = created;
    }
}