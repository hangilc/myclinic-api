package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.TextDTO;

public class TextDeleted implements PracticeLogBody {

    public TextDTO deleted;

    public TextDeleted() {
    }

    public TextDeleted(TextDTO deleted) {
        this.deleted = deleted;
    }
}
