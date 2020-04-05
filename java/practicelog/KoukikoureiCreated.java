package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KoukikoureiDTO;

public class KoukikoureiCreated implements PracticeLogBody {

    public KoukikoureiDTO created;

    public KoukikoureiCreated() {
    }

    public KoukikoureiCreated(KoukikoureiDTO created) {
        this.created = created;
    }
}