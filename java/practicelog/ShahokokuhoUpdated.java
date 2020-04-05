package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.ShahokokuhoDTO;

public class ShahokokuhoUpdated implements PracticeLogBody {

    public ShahokokuhoDTO prev;
    public ShahokokuhoDTO updated;

    public ShahokokuhoUpdated() {
    }

    public ShahokokuhoUpdated(ShahokokuhoDTO prev, ShahokokuhoDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
