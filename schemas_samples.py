"""
mutation CREATE_COMPANY{
  createUser(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    firstName: "Yaquba"
    lastName: "Kuyateh"
    streetAddress: "Street 101"
    city: "Casa"
    state: "Casa"
    zipCode: 20000
    country: "Morocco"
    isCompany: true
    isEmployee: false
    notificationIsOn: false
    phone: "888888888"
    eventType: "create_user"
    userBio: "This is a bio, balah blah"
  ){
    toReturn{
      id
      firstName
      phone
    }
  }
}
"""

"""
mutation CREATE_ORDINARY_USER{
  createUser(
<<<<<<< HEAD
    email: "yaq@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    firstName: "Yaquba"
    lastName: "Kuyateh"
    streetAddress: "Street 101"
    city: "Casa"
    state: "Casa"
    zipCode: 20000
=======
    email: "qubzen@gmail.com"
    uid: "LZWFJKeqdedqJTyVVtEUE72IkIy1"
    firstName: "Yaquba"
    lastName: "Kuyateh"
>>>>>>> 9d3de3f (Vehicle Category ready)
    country: "Morocco"
    isCompany: false
    isEmployee: false
    notificationIsOn: false
    phone: "888888888"
    eventType: "create_user"
  ){
    toReturn{
      id
      firstName
      phone
    }
  }
}
"""


"""
mutation CREATE_EMPLOYEE{
  createUser(
    email: "employeeuser12@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    firstName: "Yaquba"
    lastName: "Kuyateh"
    streetAddress: "Street 101"
    city: "Casa"
    state: "Casa"
    zipCode: 20000
    country: "Morocco"
    isCompany: false
    isEmployee: true
    notificationIsOn: false
    phone: "888888888"
    eventType: "create_user"
    userBio: "This is a bio, balah blah"
    companyId: "lt50hP8rcd2JhEBQNpMLCqwBCVRXKZYRUBacm"
    employeePosition: "Broker Agent"
  ){
    toReturn{
      id
      firstName
      phone
      
    }
  }
}
"""

"""
mutation UPDATE_EMPLOYEE{
  updateEmployee(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "update_employee"
    employeeId: "2h186hjXQW8EfUJLUL21mz1KFzf9GQRcLpZOi"
    employeePosition: "Real Estate Agent"
    showEmployee: true
  ){
    toReturn{
      id
      employeePosition
      showEmployee
      employee{
        id
      }
    }
  }
}
"""

"""
mutation SHOW_EMPLOYEES{
  showEmployees(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "show_employees"
    companyId: "bX1axrYwKELy6Bxe586WDAfEd4z5kmCl1kjcc"
    showEmployees: false
  ){
    toReturn{
      id
      showEmployees
      company{
        id
      }
    }
  }
}
"""

"""
mutation FOLLOW_USER{
  followUser(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "follow_user"
    userId: "4Nh6bF6qQxmsxC1STlYA4UVfpXO6pMXc6EfMH"
    following: "ZSC29MTZeOHMzVSFsIvM5patBMtQrWCY00C6G"
  ){
    toReturn{
      id
      activityType
    }
  }
}
"""

"""
mutation UNFOLLOW_USER{
  followUser(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "unfollow_user"
    userId: "4Nh6bF6qQxmsxC1STlYA4UVfpXO6pMXc6EfMH"
    following: "ZSC29MTZeOHMzVSFsIvM5patBMtQrWCY00C6G"
  ){
    toReturn{
      id
      activityType
    }
  }
}
"""

"""

{
  listAllUsers(filters: "{\"status\": true}"){
    lastLogin
    firstName
    email
  }
},
headers = {"Authorization": "Token token_here"}
"""


"""
mutation CREATE_A_CATEGORY{
  category(
    email: "usr@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "create_category"
    categoryName: "boat"
    categoryImageUrl: "categoryImageUrl"
  ){
    toReturn{
      id
      categoryName
      categoryImage
    }
  }
}
"""

"""
mutation DELETE_A_CATEGORY{
  category(
    email: "usr@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "delete_category"
    categoryName: "vacancy"
    categoryImageUrl: "categoryImageUrl"
  ){
    toReturn{
      id
      categoryName
      categoryImage
    }
  }
}
"""

"""
mutation CREATE_A_SUB_CATEGORY{
  subCategory(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "create_sub_category"
    categoryName: "property"
    subCategoryName: "house"
    subCategoryImageUrl: "subCategoryImageUrl"
    details:{
      price: 50000
      country: "Morocco"
      state: "Grand Casa"
      city: "Casa"
    	streetAddress: "Famous St"
      zip: 30000
    	size: 200
      plotSize: 200
      buildingSize: 200
      builtYear: 2010
      bedrooms: 5
      renovatedYear: 2022
      floors: 4
  	}    
    facilities:{
      internet: true
      dogKeepers: true
      maintenance24Hrs: true
      pool: true
      garage: true
      fireplace: true
      dogsAllowed: true
      catsAllowed: true
      poolTable: true
      mediaRoom: true
      hotTub: true
      water: true
      electricity: true
      childFriendly: true
      carWashArea: true
      gymRoom: true
      airCondition: true
      oven: true
      refrigerator: true
      microwave: true
    }
    nearby:{
      kindergarten: true
      primarySchool: true
      secondarySchool: true
      highSchool: true
      university: true
      groceryStore: true
      library: true
      cinema: true
      beach: true
      shoppingCenter: true
      nightClub: true
      theater: true
      hiking: true
      dogPark: true
      gym: true
      carWash: true
      mosque: true
      church: true
    }
  ){
    toReturn{
      id
      subCategoryName
      subCategoryImage
      details
      facilities
      nearby
      category{
        categoryName
      }
    }
  }
}
"""

"""
mutation CREATE_AD{
  createAd(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "create_ad"
    subCategoryName: "house"
    details:{
      price: 50000
      country: "Morocco"
      state: "Grand Casa"
      city: "Casa"
    	streetAddress: "Famous St"
      zip: 30000
    	size: 200
      plotSize: 200
      buildingSize: 200
      builtYear: 2010
      bedrooms: 5
      renovatedYear: 2022
      floors: 4
  	}    
    facilities:{
      internet: true
      dogKeepers: true
      maintenance24Hrs: true
      pool: true
      garage: true
      fireplace: true
      dogsAllowed: true
      catsAllowed: true
      poolTable: true
      mediaRoom: true
      hotTub: true
      water: true
      electricity: true
      childFriendly: true
      carWashArea: true
      gymRoom: true
      airCondition: true
      oven: true
      refrigerator: true
      microwave: true
    }
    nearby:{
      kindergarten: true
      primarySchool: true
      secondarySchool: true
      highSchool: true
      university: true
      groceryStore: true
      library: true
      cinema: true
      beach: true
      shoppingCenter: true
      nightClub: true
      theater: true
      hiking: true
      dogPark: true
      gym: true
      carWash: true
      mosque: true
      church: true
    }
    gallery:{
      featureImage: "featureImage_url"
      image1: "image_1"
      image2: "image_2"
      image3: "image_3"
    }
  ){
    toReturn{
      id
      details
      facilities
      nearby
      subCategory{
        subCategoryName
      }
      imageurlSet{
        adGallery
      }
      user{
        id
        firstName
        isActive
        isCompany
        isVerified
        isEmployee
      }
    }
  }
}
"""

"""
mutation UPDATE_AD{
  updateAd(
    email: "companyuser1@gmail.com"
    uid: "hjkfdkdkhhdfbmdhbjbdsnknkjf"
    eventType: "update_ad"
    isActive: true
    adId: "7UfmhIskh3SVGgQB2eR2hOWGtAfd4fJcPdufX"
    details:{
      price: 50000
      country: "Morocco"
      state: "Grand Casa"
      city: "Casa"
    	streetAddress: "Famous St"
      zip: 30000
    	size: 200
      plotSize: 200
      buildingSize: 200
      builtYear: 2010
      bedrooms: 5
      renovatedYear: 2022
      floors: 4
  	}    
    facilities:{
      internet: true
      dogKeepers: true
      maintenance24Hrs: true
      pool: true
      garage: true
      fireplace: true
      dogsAllowed: true
      catsAllowed: true
      poolTable: true
      mediaRoom: true
      hotTub: true
      water: true
      electricity: true
      childFriendly: true
      carWashArea: true
      gymRoom: true
      airCondition: true
      oven: true
      refrigerator: true
      microwave: true
    }
    nearby:{
      kindergarten: true
      primarySchool: true
      secondarySchool: true
      highSchool: true
      university: true
      groceryStore: true
      library: true
      cinema: true
      beach: true
      shoppingCenter: true
      nightClub: true
      theater: true
      hiking: true
      dogPark: true
      gym: true
      carWash: true
      mosque: true
      church: true
    }
    gallery:{
      featureImage: "featureImage_url"
      image1: "image_1"
      image2: "image_2"
      image3: "image_3"
    }
  ){
    toReturn{
      id
      details
      facilities
      nearby
      subCategory{
        subCategoryName
      }
      imageurlSet{
        adGallery
      }
      user{
        id
        firstName
        isActive
        isCompany
        isVerified
        isEmployee
      }
    }
  }
}
"""

"""
{
  adByCategory(offset: 1, subCategory: "id"){
    edges{
      node{
        id
        nearBy
        subCategory{
          id
        }
      }
    }
  }
}
"""
"""
mutation{
  publishAdByCompany(employeesId: ["NVqArjlOe2gXTTeWVC7JDOZHuub39OLrXu8Dk", "fUtnKfJXdBGhzoAg707oBOrBitbMKxYxhrb1U"], subCategoryId: "ZrfwgTnB2w5h92AfGsp44LCUzMc1PHBq2uFlL"){
    toReturn{
      id
      user{
        id
      }
    }
  }
}
"""

"""
mutation{
  updateAdToSold(adId: "ZSdtPwggzUx8g3Fh6zAeuYGuJ6BbjG4dM0CH6"){
    toReturn{
      id
      status
    }
  }
}
"""

"""
mutation{
  publishAdByEmployee(employeesId: ["id1", "id2"], subCategoryId: "id"){
    toReturn{
      id
    }
  }
}
"""


"""

{
  listAllUsers(filters: "{\"is_active\": true}"){
    lastLogin
    firstName
    email
  }
},
headers = {"Authorization": "Token token_here"}
"""

"""
{
  adByCategory(offset: 1, subCategory: "id"){
    edges{
      node{
        id
        nearBy
        subCategory{
          id
        }
      }
    }
  } 
}       
"""


"""
query ALL_ADS{
  allAds(
    subCategory_SubCategoryName: "house"
    city: "Casa"
    country: "Morocco"
    # price: 1000
    # bedrooms: 1
  ){
    edges{
      node{
        id
        details
      }
    }
  }
}
"""

"""
query REAY_AD{
  relayAd(
    id: "QWROb2RlOlVYSkw3VU9MN09Gc29GWW1nUHZqTkNJWWZzWlVURkNUSjV1UVo="
  ){
    id
    details
  }
}
"""

"""
query ADS_OF_A_USER{
  allAds(
    user_Id: "2tKjUJyNxfDic0FRz4sBGwGlzvpMvqHLP5z3k"
    subCategory_SubCategoryName_Icontains: "house"
    city: "rabat"
    country: "Morocco"
    # price: 5000
    bedrooms: 5
  ){
    edges{
      node{
        id
        details
      }
    }
  }
}
"""

"""
query SEARCH_ADS{
  allAds(
    subCategory_SubCategoryName: "house"
    city: "casa"
    state: "casa"
    country: "Morocco"
    zip: "30000"
    bedrooms: 5
    size: 200
    plotSize: 100
    buildingSize: 100
    minPrice: 1000
    maxPrice: 50000
    isActive: true
    builtYear: 2010
    renovatedYear: 2015
    kindergarten: true
    floors: 4
    # primarySchool: true
    # secondarySchool: true
    # highSchool: true
    # university: true
    # groceryStore: true
    # shoppingCenter: true
    # library: true
    # cinema: true
    # nightClub: true
    # theater: true
    # beach: true
    # hiking: true
    # dogPark: true
    # gym: true
    # carWash: true
    # mosque: true
    # church: true
    # synagogue: true
    # internet: true
    # maintenance24Hrs: true
    # pool: true
    # garage: true
    # fireplace: true
    # dogKeepers: true
    # dogsAllowed: true
    # catsAllowed: true
    # poolTable: true
    # mediaRoom: true
    # hotTub: true
    # water: true
    # electricity: true
    # childFriendly: true
    # carWashArea: true
    # gymRoom: true
    # airCondition: true
    # oven: true
    # refrigerator: true
    # microwave: true
  ){
    edges{
      node{
        # id
        details
        nearby
        facilities
      }
    }
  }
}
"""

"""
mutation{
  publishAdByCompany(employeesId: ["NVqArjlOe2gXTTeWVC7JDOZHuub39OLrXu8Dk", "fUtnKfJXdBGhzoAg707oBOrBitbMKxYxhrb1U"], subCategoryId: "ZrfwgTnB2w5h92AfGsp44LCUzMc1PHBq2uFlL"){
    toReturn{
      id
      user{
        id
      }
    }
  }
}
"""

"""
mutation{
  updateAdToSold(adId: "ZSdtPwggzUx8g3Fh6zAeuYGuJ6BbjG4dM0CH6"){
    toReturn{
      id
      status
    }
  }
}
"""

"""
mutation{
  publishAdByEmployee(employeesId: ["id1", "id2"], subCategoryId: "id"){
    toReturn{
      id
    }
  }
}
"""


"""
query FILTER_ADS{
  searchPropertyAds(
    subCategory_SubCategoryName_Contains: "house"
  	city: "OSLO"
  	# state: "casa"
  	country: "Norway"
  	# zip: "30000"
  	bedrooms: 1
  	plotSize: 100
  	# buildingSize: 100
  	minPrice: 5000
  	# maxPrice: 50000
  	# isActive: true
  	# builtYear: 2010
  	# published: true
  	# # offset: 10
  	# last: 2
    # renovatedYear: 2015
    # kindergarten: true
    # floors: 4
    # primarySchool: false
    secondarySchool: true
    highSchool: true
    # university: true
    # groceryStore: true
    # shoppingCenter: true
    # library: true
    # cinema: true
    # nightClub: true
    # theater: true
    # beach: true
    # hiking: true
    # dogPark: true
    # gym: true
    # carWash: true
    # mosque: true
    # church: true
    # synagogue: true
    # internet: true
    # maintenance24Hrs: true
    # pool: true
    # garage: true
    # fireplace: true
    # dogKeepers: true
    # dogsAllowed: true
    # catsAllowed: true
    # poolTable: true
    # mediaRoom: true
    # hotTub: true
    # water: true
    # electricity: true
    # childFriendly: true
    # carWashArea: true
    # gymRoom: true
    # airCondition: true
    # oven: true
    # refrigerator: true
    # microwave: true
  ){
    edges{
      node{
        id
        details
        nearby
        facilities
      }
    }
  }
}
"""

"""
query ALL_CATEGORIES{
  allCategories(
    categoryName: ""
  ){
    edges{
      node{
        id
        categoryName
      }
    }
  }
}
"""
