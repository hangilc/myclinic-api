package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ShahokokuhoDTO;

public class ShahokokuhoCreated implements PracticeLogBody {

    public ShahokokuhoDTO created;

    public ShahokokuhoCreated() {
    }

    public ShahokokuhoCreated(ShahokokuhoDTO created) {
        this.created = created;
    }
}
