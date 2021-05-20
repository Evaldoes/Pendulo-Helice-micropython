#include <DueTimer.h>

volatile long double Input = 0.0000;
volatile long double Output = 0.0000;
volatile long double Output1 = 0.0000;
volatile long double u[2] = {0.0000000, 0.0000000};
volatile long double y[2] = {0.0000000, 0.0000000};
volatile long double u2[12] = {0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000}; //inicialização da Variável de controle e suas posições de memória.
volatile long double y2[12] = {0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000}; //inicialização da Variável de Saída e suas posições de memória.
//volatile long double Ref[12] = {1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000};
volatile long double Ref = 1.0000;
volatile long double dRef = 0.0000;
volatile long double dy = 0.0000;

volatile int on_system = 0;
int sensorPin = A0;
int inPin = 2;
int Input_on = LOW;
int ledstate = LOW;
void setup()
{
    analogWriteResolution(12);
    analogReadResolution(12);
    Timer1.start(200000);
    Timer2.start(200000);
    Timer1.attachInterrupt(trata_adc);
    Timer2.attachInterrupt(serial_interface);

    Serial.begin(57600);
    pinMode(inPin, INPUT);
    pinMode(13, OUTPUT);
    while (true)
    {
        //    Input_on = digitalRead(inPin);
        if (digitalRead(inPin) == HIGH)
        {
            dy = 0.1;
        }
        else
        {
            dy = 0.0;
        }

        //    analogWrite(DAC0,Output1);
        digitalWrite(13, ledstate);
    }
}

void loop()
{
    // put your main code here, to run repeatedly:
}

void trata_adc()
{
    Output1 = analogRead(sensorPin);

    //y[0] = Output1;
    /*      if (on_system == 1)
      {
    Control_Loop_Conventional(Output1);
      }
      else {
    Input = 0.0000;
      }*/
    Planta_Emulada(Input);
    Output1 = (3.3000 / 4095.0000) * Output1;
    analogWrite(DAC0, (int)(4095 / 3.3) * (Output + dy));

    /*  Serial.print(Output1, 4);
    Serial.print("\t");
    Serial.println((float)(Input/3.3000), 4);
    ledstate = !ledstate;*/
}

unsigned int Planta_Emulada(volatile long double Input)
{
    u[0] = Input;
#define bo 0.019801326693245  //0.009950166250832//0.002229165999699
#define ao -0.980198673306755 //-0.990049833749168//-0.998106061172728
    y[0] = bo * u[1] - ao * y[1];

    y[1] = y[0];
    u[1] = u[0];
    Output = y[0];
    return Output;
}

void serial_interface()
{

    Serial.print((float)Output1, 4);
    Serial.print("\t");
    Serial.println((float)u[0], 4);
    le_escreve();
    ledstate = !ledstate;
}

void le_escreve()
{ //Função de Leitura de informação na Serial.

    if ((byte)Serial.available() > 0) //verifica se tem dados diponível para leitura
    {
        switch (Serial.read())
        {         //Lê o que vem de informação da serial
        case 'a': // Caso venha pela serial o caractere 'a', liga a lei de controle.
                  //        on_system = 1;
            Control_Loop_Conventional(Output1);

            break;
        case 'b': // Caso venha pela serial o caractere 'b', desliga a lei de controle.
            //        on_system = 0;
            Control_Loop_Conventional(0);
            Input = 0;
            break;
        case '0': // Caso venha pela serial o caractere '0', desliga a lei de controle.
            Ref = 1.0;
            //    Ref[0] = Ref[1] + dRef;
            //    Ref = Ref + dRef;
            Control_Loop_Conventional(Output1);
            break;
        case '1': // Caso venha pela serial o caractere '1', desliga a lei de controle.
            Ref = 1.1;
            //        Ref[0] = Ref[1] + dRef;
            //Ref = Ref + dRef;
            Control_Loop_Conventional(Output1);
            break;
        }
    }
}

/*
  volatile unsigned int Control_Loop_RST(volatile double Output) //Função que calcula a Lei de controle RST
  {
  #define ro 13.497373132934092//13.497373132934092//8.471093700565140//0.084710937005651e+2//0.134973731329341e+2//16.506736177061288//28.380178204710631
  #define r1 -13.413887388624053//-25.511889705238833//-15.674508522600506//-0.521977491428189e+2//-1.031299373426760e+2//-16.332816853653217//-28.223595380195025
  #define r2 0.0000//7.223981438940087//1.373984188198586e+2//3.488398889734969e+2//-15.764039305512549//0.0000
  #define r3 0.0000//-2.002360825043202e+2//-6.854546098278116e+2//15.591431345871722//0.0000
  #define r4 0.0000//1.744446639584724e+2//8.620635755876487e+2//0.0000
  #define r5 0.0000//-0.908278471352979e+2//-7.194391856059622e+2//0.0000
  #define r6 0.0000//0.261627859526858e+2//3.983155198327184e+2//0.0000
  #define r7 0.0000//-0.032152835973062e+2//-1.410328774909915e+2//0.0000
  #define r8 0.0000//0.289696370833011e+2//0.0000
  #define r9 0.0000//-0.026293843405182e+2//0.0000
  #define r10 0.0000
  #define r11 0.0000

  #define s1 -1.000001678937687//-1.762752011531767//-1.764608327483541//-6.077824434831100//-7.499731514173785//-2.226721865206786//-1
  #define s2 0.0000//0.762751613204359//0.764608325946674//15.772305800808963//24.885010753945849//1.462899050468401//0.0000
  #define s3 0.0000//-22.650580501897700//-47.940026079376977//-0.236176982797775//0.0000
  #define s4 0.0000//19.438331147971930//59.080884272567097//0.0000
  #define s5 0.0000//-9.967136451038593//-48.294859585546668//0.0000
  #define s6 0.0000//2.827019664004808//26.180848822294330//0.0000
  #define s7 0.0000//-0.342115225018319//-9.074580865890283//0.0000
  #define s8 0.0000//1.824565581893772//0.0000
  #define s9 0.0000//-0.162111385713350//0.0000
  #define s10 0.0000
  #define s11 0.0000

  //#define T 5.186411966562332e-8//0.001311363767245//0.156582824515606

  #define to 13.497373132934092//13.497373132934092//8.471093700565140//0.084710937005651e+2//0.134973731329341e+2//16.506736177061288//28.380178204710631
  #define t1 -13.413887388624053//-25.511889705238833//-15.674508522600506//-0.521977491428189e+2//-1.031299373426760e+2//-16.332816853653217//-28.223595380195025
  #define t2 0.0000//12.034326677137321//7.223981438940087//1.373984188198586e+2//3.488398889734969e+2//-15.764039305512549//0.0000
  #define t3 0.0000//6.853941256358021//-2.002360825043202e+2//-6.854546098278116e+2//15.591431345871722//0.0000
  #define t4 0.0000//1.744446639584724e+2//8.620635755876487e+2//0.0000
  #define t5 0.0000//-0.908278471352979e+2//-7.194391856059622e+2//0.0000
  #define t6 0.0000//0.261627859526858e+2//3.983155198327184e+2//0.0000
  #define t7 0.0000//-0.032152835973062e+2//-1.410328774909915e+2//0.0000
  #define t8 0.0000//0.289696370833011e+2//0.0000
  #define t9 0.0000//-0.026293843405182e+2//0.0000
  #define t10 0.0000
  #define t11 0.0000

  //double ya = (double)Output;

  y2[0] = (double)Output;
  double TREF = to*Ref[0] + t1*Ref[1] + t2*Ref[2] + t3*Ref[3] + t4*Ref[4] + t5*Ref[5] + t6*Ref[6] + t7*Ref[7] + t8*Ref[8] + t9*Ref[9] + t10*Ref[10] + t11*Ref[11];
  double RY = (ro * y2[0] + r1 * y2[1] + r2 * y2[2] + r3 * y2[3] + r4 * y2[4] + r5 * y2[5] + r6 * y2[6] + r7 * y2[7] + r8 * y2[8] + r9 * y2[9] + r10 * y2[10] + r11 * y2[11]);
  double SU = (s1 * u2[1] + s2 * u2[2] + s3 * u2[3] + s4 * u2[4] + s5 * u2[5] + s6 * u2[6] + s7 * u2[7] + s8 * u2[8] + s9 * u2[9] + s10 * u2[10] + s11 * u2[11]);
  u2[0] = TREF -RY -SU;

  if (u2[0] >= 5.0000){u2[0]  = 5.0000;};
  // if (u2[0] <= 0.0000){u2[0]  = 0.0000;};

  y2[11] =  y2[10];
  y2[10] =  y2[9];
  y2[9]  =  y2[8];
  y2[8]  =  y2[7];
  y2[7]  =  y2[6];
  y2[6]  =  y2[5];
  y2[5]  =  y2[4];
  y2[4]  =  y2[3];
  y2[3]  =  y2[2];
  y2[2]  =  y2[1];
  y2[1]  =  y2[0];

  u2[11] = u2[10];
  u2[10] = u2[9];
  u2[9] = u2[8];
  u2[8] = u2[7];
  u2[7] = u2[6];
  u2[6] = u2[5];
  u2[5] = u2[4];
  u2[4] = u2[3];
  u2[3] = u2[2];
  u2[2] = u2[1];
  u2[1] = u2[0];

  Ref[11] = Ref[10];
  Ref[10] = Ref[9];
  Ref[9] = Ref[8];
  Ref[8] = Ref[7];
  Ref[7] = Ref[6];
  Ref[6] = Ref[5];
  Ref[5] = Ref[4];
  Ref[4] = Ref[3];
  Ref[3] = Ref[2];
  Ref[2] = Ref[1];
  Ref[1] = Ref[0];

  Input = u2[0];
  return Input;
  }
*/

volatile unsigned int Control_Loop_Conventional(volatile long double Output) //Função que calcula a Lei de controle em Malha Direta
{
    //Define os valores do Parâmetros do controlador Digital Convencional

#define ro 4.315854441253634    //3.663265306122449//9.399233943376714//5.317998309789679
#define r1 -26.567398047958637  //-3.336734693877551//-26.282830787475476//-32.753576916231239
#define r2 69.857214031364592   //0.0000//24.431450186666414//86.171563062433719
#define r3 -101.686090295695593 //0.0000//-7.547258074881466//-125.507916379075951
#define r4 88.474521364540351   //0.0000//109.269017466283699
#define r5 -46.000839625339772  //0.0000//-56.849127512364475
#define r6 13.229817908658045   //0.0000//16.360531903894667
#define r7 -1.623079749737086   //0.0000//-2.008489899488539//0.0000
#define r8 0.0000               //0.0000
#define r9 0.0000               //0.0000
#define r10 0.0000
#define r11 0.0000

#define s1 -6.070784493603264  //-1.0000//-2.631947126594524//-6.070784493603264
#define s2 15.734412176238763  //0.0000//2.272209900217297//15.734412176238763
#define s3 -22.565869081472748 //0.0000//-0.640262769448959//-22.565869081472748
#define s4 19.337679180561445  //0.0000//19.337679180561445
#define s5 -9.900110425601737  //0.0000//-9.900110425601737
#define s6 2.803306323399506   //0.0000//2.803306323399506
#define s7 -0.338633679521965  //0.0000//-0.338633679521965
#define s8 0.0000              //0.0000
#define s9 0.0000              //0.0000
#define s10 0.0000
#define s11 0.0000

    y2[0] = (Ref)-Output;

    u2[0] = (ro * y2[0] + r1 * y2[1] + r2 * y2[2] + r3 * y2[3] + r4 * y2[4] + r5 * y2[5] + r6 * y2[6] + r7 * y2[7] + r8 * y2[8] + r9 * y2[9] + r10 * y2[10] + r11 * y2[11]) - (s1 * u2[1] + s2 * u2[2] + s3 * u2[3] + s4 * u2[4] + s5 * u2[5] + s6 * u2[6] + s7 * u2[7] + s8 * u2[8] + s9 * u2[9] + s10 * u2[10] + s11 * u2[11]);

    //    if (u2[0] >= 100.0000)u2[0] = 100.0000;
    if (u2[0] <= 0.0000)
        u2[0] = 0.0000;
    //
    y2[11] = y2[10];
    y2[10] = y2[9];
    y2[9] = y2[8];
    y2[8] = y2[7];
    y2[7] = y2[6];
    y2[6] = y2[5];
    y2[5] = y2[4];
    y2[4] = y2[3];
    y2[3] = y2[2];
    y2[2] = y2[1];
    y2[1] = y2[0];

    u2[11] = u2[10];
    u2[10] = u2[9];
    u2[9] = u2[8];
    u2[8] = u2[7];
    u2[7] = u2[6];
    u2[6] = u2[5];
    u2[5] = u2[4];
    u2[4] = u2[3];
    u2[3] = u2[2];
    u2[2] = u2[1];
    u2[1] = u2[0];

    Input = u2[0];
    return Input;
}