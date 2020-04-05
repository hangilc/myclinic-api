package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.KoukikoureiDTO;

public class KoukikoureiDeleted implements PracticeLogBody {

    public KoukikoureiDTO deleted;

    public KoukikoureiDeleted() {
    }

    public KoukikoureiDeleted(KoukikoureiDTO deleted) {
        this.deleted = deleted;
    }
}