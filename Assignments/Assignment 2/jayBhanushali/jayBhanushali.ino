  #define LILYGO_WATCH_2019_WITH_TOUCH
#include <LilyGoWatch.h>

TTGOClass *ttgo;

void setup()
{
    Serial.begin(115200);
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();

    // Clear the screen and set text properties
    ttgo->tft->fillScreen(TFT_BLACK);
    ttgo->tft->setTextColor(TFT_WHITE, TFT_BLACK);
    ttgo->tft->setTextFont(4);

    // Calculate the position to center the text
    int textWidth = ttgo->tft->textWidth("Jay Bhanushali");
    int xPos = (240 - textWidth) / 2; // Horizontal center
    int yPos = (240 - ttgo->tft->fontHeight()) / 2; // Vertical center

    // Draw "Jay Bhanushali" at the calculated position
    ttgo->tft->drawString("Jay Bhanushali", xPos, yPos);
}

void loop()
{
}
