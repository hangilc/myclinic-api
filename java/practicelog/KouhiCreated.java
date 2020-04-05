package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KouhiDTO;

public class KouhiCreated implements PracticeLogBody {

    public KouhiDTO created;

    public KouhiCreated() {
    }

    public KouhiCreated(KouhiDTO created) {
        this.created = created;
    }
}