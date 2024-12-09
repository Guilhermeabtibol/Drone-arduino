#include <Servo.h>
#include <algorithm> // Para min() e max()

// Configurações dos motores
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

// Variáveis de controle
int motorSpeed = 0; // Velocidade base dos motores
const int maxSpeed = 180; // Velocidade máxima permitida

void setup() {
    Serial.begin(9600); // Inicia a comunicação serial

    // Associação dos pinos PWM aos motores
    motor1.attach(3);
    motor2.attach(5);
    motor3.attach(6);
    motor4.attach(9);

    // Inicializando os motores com velocidade zero
    motor1.write(0);
    motor2.write(0);
    motor3.write(0);
    motor4.write(0);

    Serial.println("Drone pronto para receber comandos!");
}

void loop() {
    if (Serial.available() > 0) {
        // Lê o comando enviado pela porta serial
        String command = Serial.readStringUntil('\n');
        command.trim(); // Remove espaços extras

        if (command == "takeoff") {
            decolar();
        } else if (command == "land") {
            pousar();
        } else if (command == "forward") {
            moverFrente();
        } else if (command == "backward") {
            moverTras();
        } else if (command == "left") {
            moverEsquerda();
        } else if (command == "right") {
            moverDireita();
        } else if (command == "up") {
            subir();
        } else if (command == "down") {
            descer();
        } else {
            Serial.println("Comando não reconhecido");
        }
    }
}

// Funções para controlar o drone
void decolar() {
    motorSpeed = 100; // Define uma velocidade inicial
    ajustarMotores(motorSpeed);
    Serial.println("Drone decolando...");
}

void pousar() {
    motorSpeed = 0; // Desliga os motores
    ajustarMotores(motorSpeed);
    Serial.println("Drone pousando...");
}

void moverFrente() {
    motor1.write(motorSpeed + 20);
    motor2.write(motorSpeed + 20);
    motor3.write(motorSpeed);
    motor4.write(motorSpeed);
    Serial.println("Movendo para frente...");
}

void moverTras() {
    motor1.write(motorSpeed);
    motor2.write(motorSpeed);
    motor3.write(motorSpeed + 20);
    motor4.write(motorSpeed + 20);
    Serial.println("Movendo para trás...");
}

void moverEsquerda() {
    motor1.write(motorSpeed);
    motor2.write(motorSpeed + 20);
    motor3.write(motorSpeed + 20);
    motor4.write(motorSpeed);
    Serial.println("Movendo para a esquerda...");
}

void moverDireita() {
    motor1.write(motorSpeed + 20);
    motor2.write(motorSpeed);
    motor3.write(motorSpeed);
    motor4.write(motorSpeed + 20);
    Serial.println("Movendo para a direita...");
}

void subir() {
    motorSpeed = std::min(motorSpeed + 10, maxSpeed); // Incrementa a velocidade dos motores
    ajustarMotores(motorSpeed);
    Serial.println("Subindo...");
}

void descer() {
    motorSpeed = std::max(motorSpeed - 10, 0); // Reduz a velocidade dos motores
    ajustarMotores(motorSpeed);
    Serial.println("Descendo...");
}

void ajustarMotores(int speed) {
    motor1.write(speed);
    motor2.write(speed);
    motor3.write(speed);
    motor4.write(speed);
}

