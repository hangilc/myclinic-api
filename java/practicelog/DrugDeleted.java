package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DrugDTO;

public class DrugDeleted implements PracticeLogBody {

    public DrugDTO deleted;

    public DrugDeleted() {
    }

    public DrugDeleted(DrugDTO deleted) {
        this.deleted = deleted;
    }
}