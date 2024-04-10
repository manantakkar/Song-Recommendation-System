import { useState } from "react";

export default function Home() {
    const [data, setData] = useState(null);

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    recom(data);
  };

    // Function to handle the click event and fetch data from the API
    const recom = async (formdata) => {
      try {
        const response = await fetch('http://localhost:8000/recommend/recommend_playlist/', {
            body:formdata,
            method:"post"
        });
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

  return (
    <div className="flex">
        <section className="bg-white dark:bg-gray-900">

        <div className="py-8 px-4 mx-auto max-w-2xl lg:py-16">
            <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">Recommend me a song</h2>
            <form onSubmit={handleSubmit}>
                <div className="grid gap-4 sm:grid-cols-2 sm:gap-6">
                    <div className="sm:col-span-2">
                        <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Song name</label>
                        <input type="text" name="URL" id="URL" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Song name" required="" />
                    </div>
                     
                </div> 
                <button type="submit" className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800">
                    Submit
                </button>
            </form>
             </div>
        </section>
        {data && (
        <section className="bg-white dark:bg-gray-900">
            <h2>Fetched Data:</h2>
            <ol>
                {JSON.stringify(data).forEach(element => {
                  <li>{element}</li>  
                })}
            </ol>
        </section>
        )}
    </div>
  )
}

