package jp.chang.myclinic.logdto.practicelog;

import jp.chang.myclinic.dto.DrugDTO;

public class DrugCreated implements PracticeLogBody {

    public DrugDTO created;

    public DrugCreated() {
    }

    public DrugCreated(DrugDTO created) {
        this.created = created;
    }
}