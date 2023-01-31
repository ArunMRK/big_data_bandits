# big_data_bandits

            # msg = message.value().decode()

            # (NEW USER ENTRY)
            # if 'User' IN msg :

                # found_user == True
                # ** code for uploading user details to database **
                # user_details = e
                # user_id = get_id_from_database_for_made_user()
                # ride_id = None

            # (NEW DATA BUT NO CURRENTLY FOUND USER)
            # elif 'User' NOT IN msg AND found_user == False:

                # *skip because caught mid-stream without user*

            # (USER IS FOUND, MSG is DATA)
            # elif found_user == True AND 'User' NOT IN msg :

                # (CHECK FOR CURRENT RIDE)
                # if ride_id = None:
                    # ride_id = find_next_new_ride_id()
                    # upload_ride_data_for_id(ride_id)

                # (DATA FOR AN ALREADY ESTABLISHED RIDE)
                # if ride_id IS NOT None:
                    # upload_ride_data_for_id(ride_id)
