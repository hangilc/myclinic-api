package dev.myclinic.dto;

public class PrescExampleFullDTO {
    public PrescExampleDTO prescExample;
    public IyakuhinMasterDTO master;

    public static PrescExampleFullDTO copy(PrescExampleFullDTO src){
        PrescExampleFullDTO dst = new PrescExampleFullDTO();
        dst.prescExample = src.prescExample;
        dst.master = src.master;
        return dst;
    }

    public static PrescExampleFullDTO create(PrescExampleDTO example, IyakuhinMasterDTO master){
        PrescExampleFullDTO result = new PrescExampleFullDTO();
        result.prescExample = example;
        result.master = master;
        return result;
    }

    @Override
    public String toString() {
        return "PrescExampleFullDTO{" +
                "prescExample=" + prescExample +
                ", master=" + master +
                '}';
    }
}
