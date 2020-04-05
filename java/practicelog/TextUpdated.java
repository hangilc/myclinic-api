package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.TextDTO;

public class TextUpdated implements PracticeLogBody {

    public TextDTO prev;
    public TextDTO updated;

    public TextUpdated() {
    }

    public TextUpdated(TextDTO prev, TextDTO updated) {
        this.prev = prev;
        this.updated = updated;
    }
}
