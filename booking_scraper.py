from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_booking_data(city_name, checkin_date, checkout_date):
    with sync_playwright() as p:
        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss={city_name}&ssne={city_name}&ssne_untouched={city_name}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
                     
        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels in {city_name}.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            try:
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text(timeout=300000)
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text(timeout=30000)
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text(timeout=30000)
                hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text(timeout=30000)
                hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]
                
                # Concatenate hotel details into a single description with additional text
                hotel_dict['description'] = ('This hotel has a price of ' + hotel_dict['price'] + ', score is ' + 
                                              hotel_dict['score'] + ', average review is ' + 
                                              hotel_dict['avg review'] + ', and reviews count is ' + 
                                              hotel_dict['reviews count'])
            except Exception as e:
                print(f"Error occurred for a hotel: {e}")
                continue

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list, columns=['hotel', 'description'])
        df.to_csv(f'{city_name}_hot_list.csv', index=False) 
        
        browser.close()

if __name__ == '__main__':
    city_name = 'Goa'  # Change this to the desired city name
    checkin_date = '2024-07-01'  # Change this to the desired check-in date
    checkout_date = '2024-07-08'  # Change this to the desired check-out date
    scrape_booking_data(city_name, checkin_date, checkout_date)

