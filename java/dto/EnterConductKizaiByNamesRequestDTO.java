package dev.myclinic.dto;

public class EnterConductKizaiByNamesRequestDTO {

    public String name;
    public double amount;

    public static EnterConductKizaiByNamesRequestDTO create(String name, double amount){
        EnterConductKizaiByNamesRequestDTO result = new EnterConductKizaiByNamesRequestDTO();
        result.name = name;
        result.amount = amount;
        return result;
    }

    @Override
    public String toString() {
        return "EnterConductKizaiByNamesRequestDTO{" +
                "name='" + name + '\'' +
                ", amount=" + amount +
                '}';
    }
}
